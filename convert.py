import argparse
import sys
import time
from pathlib import Path

from utils import check_ffmpeg_installed, find_mov_files
from logger import setup_logger
from converter import VideoConverter

def parse_args():
    parser = argparse.ArgumentParser(
        description="Convert all .mov videos inside a specified folder into .mp4 format using FFmpeg."
    )
    
    parser.add_argument(
        "folder_path", 
        type=Path, 
        help="Path to the folder containing .mov files."
    )
    parser.add_argument(
        "--delete-original", 
        action="store_true", 
        help="Delete original .mov files after successful conversion."
    )
    parser.add_argument(
        "--output", 
        type=Path, 
        help="Optional output directory. If not provided, saves alongside original files."
    )
    parser.add_argument(
        "--overwrite", 
        action="store_true", 
        help="Overwrite existing .mp4 files if they exist."
    )
    parser.add_argument(
        "--verbose", 
        action="store_true", 
        help="Enable detailed logging output."
    )
    
    return parser.parse_args()

def main():
    args = parse_args()
    start_time = time.time()
    
    # 1. Setup Logger
    # Determine the directory where logs will be stored.
    # We can store logs in the current working directory under "logs"
    log_dir = Path.cwd() / "logs"
    logger = setup_logger(log_dir, args.verbose)
    
    logger.info("Starting MOV2MP4 Converter")
    logger.info(f"Target folder: {args.folder_path}")
    
    # 2. Path Validation
    if not args.folder_path.exists() or not args.folder_path.is_dir():
        logger.error(f"Error: The provided folder path '{args.folder_path}' is invalid or does not exist.")
        print(f"Error: Invalid folder path '{args.folder_path}'.", file=sys.stderr)
        sys.exit(1)
        
    # 3. Check FFmpeg
    if not check_ffmpeg_installed():
        logger.error("FFmpeg not found. Please install FFmpeg and ensure it's in your system PATH.")
        print("Error: FFmpeg is required but was not found. Please install it.", file=sys.stderr)
        sys.exit(1)
        
    # 4. Find Files
    logger.info("Scanning for .mov files...")
    mov_files = find_mov_files(args.folder_path)
    
    if not mov_files:
        logger.warning(f"No .mov files found in '{args.folder_path}'.")
        print(f"No .mov files found in '{args.folder_path}'.")
        sys.exit(0)
        
    logger.info(f"Found {len(mov_files)} .mov files.")
    
    # 5. Convert
    converter = VideoConverter(
        delete_original=args.delete_original,
        output_dir=args.output,
        overwrite=args.overwrite
    )
    
    try:
        result = converter.run(mov_files, args.folder_path)
    except KeyboardInterrupt:
        logger.error("Conversion interrupted by user.")
        print("\nConversion interrupted. Exiting...", file=sys.stderr)
        sys.exit(1)
        
    # 6. Final Summary
    end_time = time.time()
    elapsed = end_time - start_time
    # Format time taken as MM:SS
    minutes, seconds = divmod(int(elapsed), 60)
    time_taken_str = f"{minutes:02d}:{seconds:02d}"
    
    summary = (
        f"\nTotal Found: {result.total_found}\n"
        f"Converted: {result.converted}\n"
        f"Skipped: {result.skipped}\n"
        f"Failed: {result.failed}\n"
        f"Time Taken: {time_taken_str}\n"
    )
    
    print(summary)
    logger.info("Execution Summary:" + summary.replace('\n', ' - '))

if __name__ == "__main__":
    main()
