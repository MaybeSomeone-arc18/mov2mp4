import logging
import sys
from datetime import datetime
from pathlib import Path

def setup_logger(log_dir: Path, verbose: bool = False) -> logging.Logger:
    """
    Configure and setup the application logger.
    Logs are written to both a timestamped file and the console.
    
    Args:
        log_dir (Path): The directory where log files should be saved.
        verbose (bool): If True, console output will include DEBUG level messages.
        
    Returns:
        logging.Logger: The configured logger instance.
    """
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
