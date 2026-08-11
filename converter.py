import subprocess
import logging
import os
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

try:
    from tqdm import tqdm
except ImportError:
    tqdm = None

logger = logging.getLogger("mov2mp4")

@dataclass
class ConversionResult:
    total_found: int = 0
    converted: int = 0
    skipped: int = 0
    failed: int = 0
    cancelled: int = 0

class VideoConverter:
    def __init__(self, 
                 delete_original: bool = False, 
                 output_dir: Optional[Path] = None, 
                 overwrite: bool = False):
        """
        Initialize the VideoConverter.
        
        Args:
            delete_original (bool): Whether to delete original .mov files after successful conversion.
            output_dir (Path, optional): Directory to save the converted files. If None, saves in the same directory.
            overwrite (bool): Whether to overwrite existing .mp4 files.
        """
        self.delete_original = delete_original
        self.output_dir = output_dir
        self.overwrite = overwrite
        self.lock = threading.Lock()
        self.cancel_event = None

    def _get_output_path(self, input_path: Path, base_dir: Optional[Path] = None) -> Path:
        """
        Determine the output path for the converted file.
        
        Args:
            input_path (Path): Original .mov file path.
            base_dir (Path, optional): The root folder being scanned. Used to maintain relative structure 
                                       if an output_dir is specified.
        
        Returns:
            Path: The full path where the .mp4 file will be saved.
        """
        new_name = input_path.with_suffix(".mp4").name
        
        if self.output_dir:
            if base_dir:
                try:
                    rel_path = input_path.parent.relative_to(base_dir)
                    final_dir = self.output_dir / rel_path
                except ValueError:
                    final_dir = self.output_dir
            else:
                final_dir = self.output_dir
                
            final_dir.mkdir(parents=True, exist_ok=True)
            return final_dir / new_name
        else:
            return input_path.with_suffix(".mp4")

    def _convert_single(self, input_path: Path, output_path: Path, file_index: int, total_files: int, file_status_callback=None) -> str:
        """
        Process a single file: convert using FFmpeg, handle skipping and overwriting.
        
        Args:
            input_path (Path): Path to .mov file.
            output_path (Path): Path to .mp4 file.
            file_index (int): The index of this file in the queue (for display).
            total_files (int): Total number of files.
            file_status_callback (callable, optional): Callback for individual file status.
            
        Returns:
            str: Status of the conversion ('skipped', 'converted', 'failed', 'cancelled').
        """
        if self.cancel_event and self.cancel_event.is_set():
            return "cancelled"

        filename = input_path.name
        header_msg = f"[{file_index}/{total_files}] Converting {filename}..."
        
        if tqdm:
            tqdm.write(header_msg)
        else:
            print(header_msg)
            
        logger.info(f"Starting conversion: {input_path} -> {output_path}")
        
        if file_status_callback:
            file_status_callback(input_path, "converting")
        
        if output_path.exists() and not self.overwrite:
            msg = "✗ Skipped (File exists)"
            if tqdm:
                tqdm.write(msg + "\n")
            else:
                print(msg + "\n")
            logger.info(f"Skipped {input_path} (Output file already exists)")
            return "skipped"

        # Construct FFmpeg command
        # -y : overwrite output files (we handle overwrite logic ourselves, but pass -y so ffmpeg doesn't block)
        # -loglevel error : reduce ffmpeg verbosity unless it's an error
        cmd = [
            "ffmpeg", "-y", "-i", str(input_path), 
            "-vcodec", "libx264", "-crf", "23", # standard high-quality h264 settings
            "-acodec", "aac", "-b:a", "192k",   # good audio quality
            "-loglevel", "error",
            str(output_path)
        ]
        
        try:
            # Use Popen to allow cancellation
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # Poll the process, waiting for it to finish or for cancel_event to be set
            while proc.poll() is None:
                if self.cancel_event and self.cancel_event.is_set():
                    proc.terminate()
                    proc.wait() # Ensure it's dead
                    logger.info(f"Conversion cancelled for: {filename}")
                    
                    # Clean up partial output file if we cancelled
                    if output_path.exists():
                        try:
                            output_path.unlink()
                        except OSError:
                            pass
                            
                    return "cancelled"
                    
                # Small wait to prevent busy looping
                if self.cancel_event:
                    self.cancel_event.wait(0.2)
                else:
                    try:
                        proc.wait(timeout=0.2)
                    except subprocess.TimeoutExpired:
                        pass
            
            # Process finished naturally
            if proc.returncode == 0:
                msg = "✓ Completed"
                logger.info(f"Successfully converted: {filename}")
                
                if self.delete_original:
                    try:
                        input_path.unlink()
                        logger.info(f"Deleted original file: {input_path}")
                    except OSError as e:
                        logger.error(f"Failed to delete original file {input_path}: {e}")
                        
                status = "converted"
            else:
                msg = "✗ Failed"
                stderr_output = proc.stderr.read().strip()
                logger.error(f"FFmpeg failed for {filename}. Error: {stderr_output}")
                status = "failed"
                
        except Exception as e:
            msg = "✗ Failed"
            logger.error(f"Exception during conversion of {filename}: {str(e)}")
            status = "failed"

        if tqdm:
            tqdm.write(msg + "\n")
        else:
            print(msg + "\n")
            
        return status

    def run(self, files: List[Path], base_dir: Path, progress_callback=None, file_status_callback=None) -> ConversionResult:
        """
        Execute the batch conversion process using multithreading.
        
        Args:
            files (List[Path]): List of .mov files to convert.
            base_dir (Path): The root directory, used to calculate relative output paths.
            progress_callback (callable, optional): A callback function called after each file completes, 
                                                    passing the current ConversionResult.
            file_status_callback (callable, optional): A callback function called when a file's status changes.
            
        Returns:
            ConversionResult: The summary of the conversion process.
        """
        result = ConversionResult(total_found=len(files))
        if result.total_found == 0:
            return result
            
        # Limit max threads to avoid overwhelming the system
        max_workers = min(32, (os.cpu_count() or 1) + 4)
        # However, for CPU intensive tasks like ffmpeg, it's better to use fewer threads
        max_workers = max(1, (os.cpu_count() or 2) // 2)

        pbar = None
        if tqdm:
            pbar = tqdm(total=result.total_found, desc="Total Progress", unit="file")

        # We will dispatch futures. To keep the 1/N indexing correct we attach the index.
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_file = {}
            for i, file_path in enumerate(files, 1):
                out_path = self._get_output_path(file_path, base_dir)
                future = executor.submit(self._convert_single, file_path, out_path, i, result.total_found, file_status_callback)
                future_to_file[future] = file_path

            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    status = future.result()
                    with self.lock:
                        if status == "converted":
                            result.converted += 1
                        elif status == "skipped":
                            result.skipped += 1
                        elif status == "cancelled":
                            result.cancelled += 1
                        else:
                            result.failed += 1
                except Exception as exc:
                    logger.error(f"File {file_path.name} generated an exception: {exc}")
                    with self.lock:
                        result.failed += 1
                        
                if pbar:
                    pbar.update(1)
                    
                if progress_callback:
                    with self.lock:
                        # Copy the current result so we don't pass a mutating object across threads 
                        # if the callback queues it to another thread without a lock
                        from copy import copy
                        current_res = copy(result)
                    progress_callback(current_res)
                
                if file_status_callback:
                    file_status_callback(file_path, status)
                    
        if pbar:
            pbar.close()

        return result
