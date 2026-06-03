"use client";

import { useState, useRef } from "react";
import { useRouter } from "next/navigation";
import { UploadCloud, FileVideo, X } from "lucide-react";
import axios from "axios";

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const router = useRouter();

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const droppedFile = e.dataTransfer.files[0];
      if (droppedFile.name.toLowerCase().endsWith(".mov")) {
        setFile(droppedFile);
      } else {
        alert("Only .mov files are supported");
      }
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    
    setIsUploading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("http://localhost:8000/api/v1/upload", formData, {
        onUploadProgress: (progressEvent) => {
          if (progressEvent.total) {
            const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
            setUploadProgress(percentCompleted);
          }
        },
      });

      const { job_id } = response.data;
      
      // Start the conversion job
      await axios.post(`http://localhost:8000/api/v1/convert/${job_id}`);
      
      // Redirect to tracking page
      router.push(`/conversion/${job_id}`);
    } catch (error) {
      console.error("Upload failed", error);
      alert("Failed to upload the file. Please try again.");
      setIsUploading(false);
      setUploadProgress(0);
    }
  };

  return (
    <div className="min-h-screen bg-black text-white flex items-center justify-center p-6 relative overflow-hidden">
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-purple-900/20 rounded-full blur-[120px] pointer-events-none"></div>

      <div className="w-full max-w-2xl z-10">
        <div className="text-center mb-10">
          <h1 className="text-4xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-blue-400">
            Upload Your Video
          </h1>
          <p className="text-gray-400">Select a .MOV file to begin the lightning-fast conversion to MP4.</p>
        </div>

        <div 
          className={`border-2 border-dashed rounded-3xl p-12 text-center transition-all duration-300 ${isDragging ? 'border-purple-500 bg-purple-500/10' : 'border-white/20 bg-white/5 hover:border-white/40 hover:bg-white/10'} backdrop-blur-md`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          {!file ? (
            <div className="flex flex-col items-center justify-center cursor-pointer" onClick={() => fileInputRef.current?.click()}>
              <div className="w-20 h-20 rounded-full bg-white/10 flex items-center justify-center mb-6">
                <UploadCloud className="w-10 h-10 text-purple-400" />
              </div>
              <h3 className="text-2xl font-semibold mb-2">Drag & Drop your MOV here</h3>
              <p className="text-gray-400 mb-6">or click to browse from your computer</p>
              <button className="px-6 py-3 bg-white/10 hover:bg-white/20 rounded-full text-white font-medium transition-colors">
                Select File
              </button>
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center">
              <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-purple-500 to-blue-500 flex items-center justify-center mb-6 relative">
                <FileVideo className="w-10 h-10 text-white" />
                {!isUploading && (
                  <button 
                    className="absolute -top-3 -right-3 w-8 h-8 bg-red-500 hover:bg-red-600 rounded-full flex items-center justify-center transition-colors"
                    onClick={(e) => { e.stopPropagation(); setFile(null); }}
                  >
                    <X className="w-4 h-4 text-white" />
                  </button>
                )}
              </div>
              <h3 className="text-xl font-semibold mb-2 truncate max-w-xs">{file.name}</h3>
              <p className="text-gray-400 mb-8">{(file.size / (1024 * 1024)).toFixed(2)} MB</p>

              {isUploading ? (
                <div className="w-full max-w-sm">
                  <div className="flex justify-between text-sm mb-2">
                    <span>Uploading...</span>
                    <span>{uploadProgress}%</span>
                  </div>
                  <div className="h-2 w-full bg-white/10 rounded-full overflow-hidden">
                    <div 
                      className="h-full bg-gradient-to-r from-purple-500 to-blue-500 transition-all duration-300" 
                      style={{ width: `${uploadProgress}%` }}
                    ></div>
                  </div>
                </div>
              ) : (
                <button 
                  onClick={handleUpload}
                  className="px-8 py-4 bg-white text-black hover:scale-105 transition-transform font-bold rounded-full shadow-[0_0_20px_rgba(255,255,255,0.2)]"
                >
                  Start Conversion
                </button>
              )}
            </div>
          )}
          
          <input 
            type="file" 
            ref={fileInputRef} 
            onChange={handleFileChange} 
            accept=".mov,video/quicktime" 
            className="hidden" 
          />
        </div>
      </div>
    </div>
  );
}
