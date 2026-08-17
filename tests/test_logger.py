import unittest
import sys
import os
import logging
from pathlib import Path
import tempfile
import shutil

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from logger import get_default_log_dir, setup_logger

class TestLogger(unittest.TestCase):
    def test_get_default_log_dir_location(self):
        log_dir = get_default_log_dir()
        self.assertIsInstance(log_dir, Path)

        # On Windows, logs must be in per-user writable location, NEVER Program Files
        if sys.platform.startswith("win"):
            log_dir_str = str(log_dir).lower()
            self.assertNotIn("program files", log_dir_str)
            self.assertNotIn("program files (x86)", log_dir_str)

            local_app_data = os.environ.get("LOCALAPPDATA", "")
            if local_app_data:
                self.assertTrue(log_dir_str.startswith(local_app_data.lower()))
            self.assertTrue(log_dir_str.endswith(os.path.join("mov2mp4", "logs").lower()))
        elif sys.platform == "darwin":
            log_dir_str = str(log_dir)
            self.assertTrue(log_dir_str.endswith("Library/Logs/MOV2MP4"))

    def test_setup_logger_creates_directory_and_file(self):
        temp_dir = Path(tempfile.mkdtemp())
        try:
            target_dir = temp_dir / "nested" / "logs"
            logger = setup_logger(log_dir=target_dir)
            self.assertTrue(target_dir.exists())
            self.assertTrue(target_dir.is_dir())

            log_files = list(target_dir.glob("convert_*.log"))
            self.assertGreaterEqual(len(log_files), 1)
        finally:
            # Close file handlers before cleanup
            for handler in logging.getLogger("mov2mp4").handlers[:]:
                handler.close()
                logging.getLogger("mov2mp4").removeHandler(handler)
            shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    unittest.main()
