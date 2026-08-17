import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

def get_default_log_dir() -> Path:
    r"""
    Returns a platform-appropriate, per-user writable directory for log files.
    - Windows: %LOCALAPPDATA%\MOV2MP4\logs
    - macOS: ~/Library/Logs/MOV2MP4
    - Linux/Other: ~/.local/share/MOV2MP4/logs
    """
    if sys.platform.startswith("win"):
        local_app_data = os.environ.get("LOCALAPPDATA")
        if local_app_data:
            base_dir = Path(local_app_data)
        else:
            base_dir = Path.home() / "AppData" / "Local"
        return base_dir / "MOV2MP4" / "logs"
    elif sys.platform == "darwin":
        return Path.home() / "Library" / "Logs" / "MOV2MP4"
    else:
        return Path.home() / ".local" / "share" / "MOV2MP4" / "logs"

def setup_logger(log_dir: Optional[Path] = None, verbose: bool = False) -> logging.Logger:
    """
    Configure and setup the application logger.
    Logs are written to both a timestamped file and the console.
    
    Args:
        log_dir (Optional[Path]): Directory where log files are saved. Defaults to get_default_log_dir().
        verbose (bool): If True, console output will include DEBUG level messages.
        
    Returns:
        logging.Logger: The configured logger instance.
    """
    if log_dir is None:
        log_dir = get_default_log_dir()

    log_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"convert_{timestamp}.log"
    
    logger = logging.getLogger("mov2mp4")
    logger.setLevel(logging.DEBUG)  # Capture everything at the root logger level
    
    # Prevent adding handlers multiple times if setup_logger is called again
    if logger.hasHandlers():
        logger.handlers.clear()
        
    # Formatter for log messages
    file_formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)-8s - %(message)s", 
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_formatter = logging.Formatter(
        "%(levelname)s: %(message)s"
    )
    
    # File Handler
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)
    
    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG if verbose else logging.INFO)
    console_handler.setFormatter(console_formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger
