from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import uuid
from typing import Dict
from worker.tasks import convert_video_task
from core.config import settings
from celery.result import AsyncResult
import asyncio
import json

api_router = APIRouter()

# In-memory storage for active websocket connections (mocking a pubsub system for now)
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, job_id: str):
        await websocket.accept()
        self.active_connections[job_id] = websocket

    def disconnect(self, job_id: str):
        if job_id in self.active_connections:
            del self.active_connections[job_id]

    async def send_personal_message(self, message: dict, job_id: str):
        if job_id in self.active_connections:
            await self.active_connections[job_id].send_json(message)

manager = ConnectionManager()

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

class JobResponse(BaseModel):
    job_id: str
    status: str

@api_router.post("/upload", response_model=JobResponse)
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".mov"):
        raise HTTPException(status_code=400, detail="Only .mov files are supported.")
        
    job_id = str(uuid.uuid4())
    input_path = os.path.join(settings.UPLOAD_DIR, f"{job_id}.mov")
    
    with open(input_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
        
    return {"job_id": job_id, "status": "uploaded"}

@api_router.post("/convert/{job_id}", response_model=JobResponse)
async def start_conversion(job_id: str):
    input_path = os.path.join(settings.UPLOAD_DIR, f"{job_id}.mov")
    output_path = os.path.join(settings.UPLOAD_DIR, f"{job_id}.mp4")
    
    if not os.path.exists(input_path):
        raise HTTPException(status_code=404, detail="Uploaded file not found.")
        
    # Dispatch Celery Task
    task = convert_video_task.apply_async(
        args=[input_path, output_path, job_id],
        task_id=job_id # Use the same job_id for celery task_id
    )
    
    return {"job_id": job_id, "status": "queued"}

@api_router.get("/status/{job_id}")
async def get_status(job_id: str):
    task_result = AsyncResult(job_id)
    return {
        "job_id": job_id,
        "status": task_result.state,
        "result": task_result.result if task_result.ready() else None
    }

@api_router.get("/download/{job_id}")
async def download_file(job_id: str):
    output_path = os.path.join(settings.UPLOAD_DIR, f"{job_id}.mp4")
    if not os.path.exists(output_path):
        raise HTTPException(status_code=404, detail="Converted file not found. It might have expired.")
        
    return FileResponse(
        path=output_path, 
        filename=f"converted_{job_id}.mp4", 
        media_type='video/mp4'
    )

@api_router.websocket("/ws/progress/{job_id}")
async def websocket_endpoint(websocket: WebSocket, job_id: str):
    await manager.connect(websocket, job_id)
    try:
        while True:
            # In a real system, you'd subscribe to Redis pub/sub from Celery here
            # For simplicity, we just poll Celery task state and push to the client
            task_result = AsyncResult(job_id)
            state = task_result.state
            
            await manager.send_personal_message({"job_id": job_id, "status": state}, job_id)
            
            if state in ["SUCCESS", "FAILURE"]:
                break
                
            await asyncio.sleep(1) # Poll every second
    except WebSocketDisconnect:
        manager.disconnect(job_id)
