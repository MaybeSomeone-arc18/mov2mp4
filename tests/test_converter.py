import unittest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from converter import VideoConverter, ConversionResult

class TestConverter(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.base_dir = Path(self.test_dir)
        
    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_get_output_path_same_dir(self):
        converter = VideoConverter()
        input_path = self.base_dir / "test.mov"
        out_path = converter._get_output_path(input_path, self.base_dir)
        self.assertEqual(out_path, self.base_dir / "test.mp4")

    def test_get_output_path_custom_dir(self):
        out_dir = self.base_dir / "output"
        converter = VideoConverter(output_dir=out_dir)
        
        # Mock file in a subfolder
        input_path = self.base_dir / "sub" / "test.mov"
        out_path = converter._get_output_path(input_path, self.base_dir)
        
        self.assertEqual(out_path, out_dir / "sub" / "test.mp4")

    @patch("subprocess.run")
    def test_convert_single_success(self, mock_run):
        # Setup mock for subprocess
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_run.return_value = mock_process
        
        converter = VideoConverter()
        input_path = self.base_dir / "test.mov"
        input_path.touch()
        
        out_path = self.base_dir / "test.mp4"
        
        status = converter._convert_single(input_path, out_path, 1, 1)
        
        self.assertEqual(status, "converted")
        mock_run.assert_called_once()
        
    @patch("subprocess.run")
    def test_convert_single_failure(self, mock_run):
        # Setup mock for subprocess
        mock_process = MagicMock()
        mock_process.returncode = 1
        mock_process.stderr = "FFmpeg error"
        mock_run.return_value = mock_process
        
        converter = VideoConverter()
        input_path = self.base_dir / "test.mov"
        input_path.touch()
        
        out_path = self.base_dir / "test.mp4"
        
        status = converter._convert_single(input_path, out_path, 1, 1)
        
        self.assertEqual(status, "failed")

    def test_convert_single_skip_existing(self):
        converter = VideoConverter(overwrite=False)
        input_path = self.base_dir / "test.mov"
        input_path.touch()
        
        out_path = self.base_dir / "test.mp4"
        out_path.touch() # Create existing output file
        
        status = converter._convert_single(input_path, out_path, 1, 1)
        self.assertEqual(status, "skipped")

    @patch("subprocess.run")
    def test_delete_original(self, mock_run):
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_run.return_value = mock_process
        
        converter = VideoConverter(delete_original=True)
        input_path = self.base_dir / "test.mov"
        input_path.touch()
        out_path = self.base_dir / "test.mp4"
        
        self.assertTrue(input_path.exists())
        
        converter._convert_single(input_path, out_path, 1, 1)
        
        self.assertFalse(input_path.exists())

if __name__ == "__main__":
    unittest.main()
