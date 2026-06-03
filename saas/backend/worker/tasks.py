import subprocess
import os
from pathlib import Path
from celery import shared_task
from worker.celery_app import celery_app
from core.config import settings
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, name="convert_video")
def convert_video_task(self, input_filepath: str, output_filepath: str, job_id: str):
    """
    Background task to convert a video using FFmpeg.
    """
    logger.info(f"Starting conversion job {job_id}")
    self.update_state(state="PROGRESS", meta={"status": "processing"})
    
    cmd = [
        "ffmpeg", "-y", "-i", input_filepath,
        "-vcodec", "libx264", "-crf", "23",
        "-acodec", "aac", "-b:a", "192k",
        "-loglevel", "error",
        output_filepath
    ]
    
    try:
        # Run ffmpeg synchronously in this celery worker thread
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            logger.info(f"Successfully converted job {job_id}")
            
            # Clean up original file to save space
            try:
                os.remove(input_filepath)
            except OSError:
                pass
                
            return {"status": "completed", "job_id": job_id, "output": output_filepath}
        else:
            logger.error(f"FFmpeg failed for {job_id}. Error: {result.stderr}")
            # Raise exception to trigger Celery retry/failure mechanism
            raise Exception(f"FFmpeg Error: {result.stderr}")
    except Exception as exc:
        logger.exception(f"Exception in job {job_id}")
        raise exc
