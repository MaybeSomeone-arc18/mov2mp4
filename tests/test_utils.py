import unittest
from pathlib import Path
import tempfile
import shutil
import os
from unittest.mock import patch

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils import find_mov_files, check_ffmpeg_installed

class TestUtils(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_find_mov_files(self):
        # Create dummy files
        Path(self.test_dir, "video1.mov").touch()
        Path(self.test_dir, "video2.MOV").touch()  # Test case insensitivity
        Path(self.test_dir, "image.jpg").touch()
        Path(self.test_dir, "audio.mp3").touch()
        
        # Subdirectory
        sub_dir = Path(self.test_dir, "sub")
        sub_dir.mkdir()
        Path(sub_dir, "video3.mov").touch()
        
        files = find_mov_files(Path(self.test_dir))
        
        self.assertEqual(len(files), 3)
        file_names = {f.name for f in files}
        self.assertEqual(file_names, {"video1.mov", "video2.MOV", "video3.mov"})

    def test_find_mov_files_invalid_path(self):
        files = find_mov_files(Path(self.test_dir, "nonexistent"))
        self.assertEqual(files, [])

    @patch("shutil.which")
    def test_check_ffmpeg_installed_true(self, mock_which):
        mock_which.return_value = "/usr/bin/ffmpeg"
        self.assertTrue(check_ffmpeg_installed())

    @patch("shutil.which")
    def test_check_ffmpeg_installed_false(self, mock_which):
        mock_which.return_value = None
        self.assertFalse(check_ffmpeg_installed())

if __name__ == "__main__":
    unittest.main()
