"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { Loader2, Download, CheckCircle, XCircle } from "lucide-react";

export default function ConversionProgressPage() {
  const params = useParams();
  const job_id = params.job_id as string;
  
  const [status, setStatus] = useState<string>("connecting");

  useEffect(() => {
    if (!job_id) return;

    // Connect to FastAPI WebSocket
    const ws = new WebSocket(`ws://localhost:8000/api/v1/ws/progress/${job_id}`);

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.status) {
        setStatus(data.status);
      }
    };

    ws.onclose = () => {
      console.log("WebSocket disconnected");
    };

    return () => {
      ws.close();
    };
  }, [job_id]);

  const handleDownload = () => {
    // Trigger download from backend
    window.location.href = `http://localhost:8000/api/v1/download/${job_id}`;
  };

  return (
    <div className="min-h-screen bg-black text-white flex items-center justify-center p-6 relative overflow-hidden">
      <div className="w-full max-w-lg z-10 p-12 rounded-3xl bg-white/5 border border-white/10 backdrop-blur-md text-center">
        
        {status === "connecting" || status === "PENDING" || status === "PROGRESS" || status === "queued" ? (
          <>
            <div className="relative w-24 h-24 mx-auto mb-8">
              <div className="absolute inset-0 rounded-full border-4 border-white/10"></div>
              <div className="absolute inset-0 rounded-full border-4 border-purple-500 border-t-transparent animate-spin"></div>
              <div className="absolute inset-0 flex items-center justify-center">
                <Loader2 className="w-8 h-8 text-purple-400 animate-pulse" />
              </div>
            </div>
            
            <h2 className="text-3xl font-bold mb-4">Converting...</h2>
            <p className="text-gray-400">
              Our servers are hard at work processing your video. 
              Please don't close this page.
            </p>
          </>
        ) : status === "SUCCESS" || status === "completed" ? (
          <>
            <div className="w-24 h-24 rounded-full bg-green-500/20 flex items-center justify-center mx-auto mb-8">
              <CheckCircle className="w-12 h-12 text-green-400" />
            </div>
            
            <h2 className="text-3xl font-bold mb-4">Ready to Download!</h2>
            <p className="text-gray-400 mb-8">Your MOV file was successfully converted to MP4.</p>
            
            <button 
              onClick={handleDownload}
              className="inline-flex items-center justify-center gap-3 w-full py-4 bg-white text-black font-bold rounded-full hover:scale-105 transition-transform"
            >
              <Download className="w-5 h-5" />
              Download MP4
            </button>
          </>
        ) : (
          <>
            <div className="w-24 h-24 rounded-full bg-red-500/20 flex items-center justify-center mx-auto mb-8">
              <XCircle className="w-12 h-12 text-red-400" />
            </div>
            
            <h2 className="text-3xl font-bold mb-4">Conversion Failed</h2>
            <p className="text-gray-400 mb-8">An error occurred while processing your video. Please try again later.</p>
            
            <button 
              onClick={() => window.location.href = '/upload'}
              className="inline-flex items-center justify-center gap-3 w-full py-4 bg-white/10 hover:bg-white/20 text-white font-bold rounded-full transition-colors"
            >
              Try Another File
            </button>
          </>
        )}

      </div>
    </div>
  );
}
