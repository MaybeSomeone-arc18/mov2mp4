import sys
import os
from pathlib import Path
import logging

logger = logging.getLogger("mov2mp4.runtime")

def setup_environment():
    """
    Detects if the application is running as a frozen PyInstaller bundle.
    If so, it locates the bundled FFmpeg binary directory inside sys._MEIPASS 
    and prepends it to the system PATH.
    
    This ensures that unmodified subprocess calls to 'ffmpeg' in converter.py 
    will automatically use the bundled executable without altering normal development behavior.
    """
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        bundle_dir = Path(sys._MEIPASS)
        bin_dir = bundle_dir / "bin"
        
        if bin_dir.exists():
            # Prepend the bundled bin directory to PATH
            os.environ["PATH"] = f"{bin_dir}{os.pathsep}{os.environ.get('PATH', '')}"
            
            # Update permissions just in case (macOS/Linux)
            ffmpeg_path = bin_dir / "ffmpeg"
            if ffmpeg_path.exists() and os.name != 'nt':
                try:
                    os.chmod(ffmpeg_path, 0o755)
                except Exception as e:
                    logger.warning(f"Could not set execute permissions on bundled ffmpeg: {e}")
