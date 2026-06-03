# MOV2MP4 Converter

A production-ready Python CLI application that batch converts `.mov` video files to `.mp4` format using FFmpeg.

## Features

- **Recursive Scanning**: Automatically finds all `.mov` files within a specified directory and its subdirectories.
- **Multithreading**: Utilizes concurrent threads to convert multiple videos simultaneously for faster processing.
- **Progress Tracking**: Displays a clean, real-time progress bar (via `tqdm`) along with individual file status.
- **Smart Output Handling**: Replicates the original folder structure if a custom output directory is specified.
- **Safe Conversion**: Skips files that have already been converted unless explicitly told to overwrite.
- **Comprehensive Logging**: Generates timestamped logs with detailed information on each conversion run.

## Requirements

- Python 3.11+
- FFmpeg installed and accessible in the system PATH.
- `tqdm` (for progress bars)

## Installation

1. **Clone the repository or download the source code.**
2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Install FFmpeg:**
   - **macOS (using Homebrew):** `brew install ffmpeg`
   - **Ubuntu/Debian:** `sudo apt install ffmpeg`
   - **Windows:** Download from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) or use `winget install ffmpeg` and add it to your System PATH.

## Usage

Basic usage requires only the target folder path:

```bash
python convert.py /path/to/videos
```

### Desktop GUI (No Terminal Required)

If you prefer a visual interface, you can run the Tkinter GUI:

```bash
python gui.py
```
This will open a desktop window where you can select folders using a visual file browser and click a button to convert.

### CLI Options

- `folder_path` (Required): The root directory to scan for `.mov` files.
- `--delete-original`: Deletes the original `.mov` files after they are successfully converted.
- `--output <path>`: Specifies a custom directory to save the converted `.mp4` files. The original folder hierarchy will be preserved inside this directory.
- `--overwrite`: Forces FFmpeg to overwrite existing `.mp4` files. By default, existing files are skipped.
- `--verbose`: Enables debug-level logging output in the console.

### Examples

**1. Basic conversion in place:**
```bash
python convert.py ./videos
```

**2. Convert and delete original files:**
```bash
python convert.py ./videos --delete-original
```

**3. Save converted files to a separate directory:**
```bash
python convert.py ./videos --output ./converted_videos
```

**4. Force overwrite and show detailed logs:**
```bash
python convert.py ./videos --overwrite --verbose
```

## Troubleshooting

- **`Error: FFmpeg is required but was not found.`**
  Ensure FFmpeg is installed correctly. Try running `ffmpeg -version` in your terminal. If it's not recognized, you need to add FFmpeg's `bin` folder to your system's PATH environment variable.
- **`PermissionError` or files not converting:**
  Ensure you have read and write access to both the source folder and the destination folder.
- **System slowing down during conversion:**
  The tool uses multithreading up to half of your available CPU cores. Video conversion is CPU intensive.

## Running Tests

Unit tests are provided for core functionalities. From the root directory, run:

```bash
python -m unittest discover tests
```
