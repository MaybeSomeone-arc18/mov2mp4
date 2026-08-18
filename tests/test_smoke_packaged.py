import unittest
import os
import sys
import subprocess
import tempfile
import shutil
from pathlib import Path

class TestPackagedAppSmoke(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.dist_dir = Path(__file__).resolve().parent.parent / "dist" / "MOV2MP4"
        
        self.exe_path = self.dist_dir / "MOV2MP4.exe"
        
        # FFmpeg could be in _internal/bin or bin depending on PyInstaller version
        self.ffmpeg_path = self.dist_dir / "_internal" / "bin" / "ffmpeg.exe"
        if not self.ffmpeg_path.exists():
            self.ffmpeg_path = self.dist_dir / "bin" / "ffmpeg.exe"

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    @unittest.skipUnless(sys.platform.startswith('win'), "Packaged smoke test is Windows-only for MOV2MP4.exe")
    def test_packaged_conversion(self):
        # 1. The packaged MOV2MP4 executable exists.
        self.assertTrue(self.exe_path.exists(), f"MOV2MP4.exe not found at {self.exe_path}")
        
        # 2. The bundled FFmpeg executable exists.
        self.assertTrue(self.ffmpeg_path.exists(), f"Bundled ffmpeg.exe not found at {self.ffmpeg_path}")
        
        # 3. Bundled FFmpeg can execute.
        result = subprocess.run([str(self.ffmpeg_path), "-version"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, f"FFmpeg failed to execute: {result.stderr}")
        self.assertIn("ffmpeg version", result.stdout)
        
        # 4. A small valid MOV test input can be generated.
        test_mov = Path(self.test_dir) / "smoke_test.mov"
        gen_cmd = [
            str(self.ffmpeg_path), 
            "-f", "lavfi", 
            "-i", "testsrc=duration=1:size=320x240:rate=30",
            "-vcodec", "qtrle",
            str(test_mov)
        ]
        result = subprocess.run(gen_cmd, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, f"Failed to generate test.mov: {result.stderr}")
        self.assertTrue(test_mov.exists(), "Test MOV was not created")
        self.assertGreater(test_mov.stat().st_size, 0, "Test MOV is empty")
        
        # 5. MOV2MP4 can convert it to MP4 using the packaged environment.
        app_cmd = [str(self.exe_path), "--headless-test", str(self.test_dir)]
        result = subprocess.run(app_cmd, capture_output=True, text=True)
        
        # 8. A failed test produces a useful CI error.
        self.assertEqual(result.returncode, 0, f"Packaged conversion failed.\nStdout: {result.stdout}\nStderr: {result.stderr}")
        
        # 6. The resulting MP4 exists.
        test_mp4 = Path(self.test_dir) / "smoke_test.mp4"
        self.assertTrue(test_mp4.exists(), "Output MP4 was not created")
        
        # 7. The resulting MP4 is non-empty.
        self.assertGreater(test_mp4.stat().st_size, 0, "Output MP4 is empty")

if __name__ == "__main__":
    unittest.main()
