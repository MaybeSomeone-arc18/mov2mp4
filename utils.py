import shutil
import logging
from pathlib import Path
from typing import List

logger = logging.getLogger("mov2mp4")

def check_ffmpeg_installed() -> bool:
    """
    Check if FFmpeg is installed and accessible from the system PATH.
    
    Returns:
        bool: True if FFmpeg is installed, False otherwise.
    """
    return shutil.which("ffmpeg") is not None

def find_mov_files(directory: Path) -> List[Path]:
    """
    Recursively scan a directory to find all .mov files.
    
    Args:
        directory (Path): The root directory to scan.
        
    Returns:
        List[Path]: A list of Path objects for each .mov file found.
    """
    if not directory.exists() or not directory.is_dir():
        logger.error(f"Invalid directory: {directory}")
        return []
    
    # Using rglob to perform a recursive search for .mov files
    # We do a case-insensitive match by checking the suffix, 
    # though rglob is case-sensitive on some OS.
    # To be perfectly safe across OS, we can just grab all files and filter by suffix.
    mov_files = [p for p in directory.rglob("*") if p.is_file() and p.suffix.lower() == ".mov"]
    return mov_files
