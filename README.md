# 🎬 MOV2MP4 Converter

[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/MaybeSomeone-arc18/mov2mp4)

A fast, production-ready Python tool that batch converts `.mov` video files to `.mp4` format using FFmpeg. It comes with both a powerful Command Line Interface (CLI) and a sleek, modern Desktop GUI.

---

## ✨ Key Features

- **Modern Desktop GUI**: A beautiful, native-feeling dark/light mode interface built with `customtkinter`.
- **Recursive Folder Scanning**: Automatically finds all `.mov` files within a specified directory and its sub-folders.
- **Lightning Fast (Multithreading)**: Utilizes concurrent threads to convert multiple videos simultaneously.
- **Real-Time Progress Tracking**: 
  - *CLI*: Displays a clean progress bar via `tqdm`.
  - *GUI*: Features a visual progress bar and live file-count updates.
- **Smart Output Handling**: Automatically replicates your original folder structure if you specify a custom output directory.
- **Safe Conversion**: Skips previously converted files to save time, unless you explicitly choose to `--overwrite`.
- **Comprehensive Logging**: Generates timestamped logs with detailed information on each run.

---

## 🚀 Quick Start

### 1. Prerequisites
- **Python 3.11+**
- **FFmpeg**: Must be installed and accessible in your system PATH.
  - *macOS*: `brew install ffmpeg`
  - *Ubuntu/Debian*: `sudo apt install ffmpeg`
  - *Windows*: Download from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) or run `winget install ffmpeg`

### 2. Installation
Clone the repository and install the required dependencies:
```bash
git clone https://github.com/MaybeSomeone-arc18/mov2mp4.git
cd mov2mp4
pip install -r requirements.txt
```
*(Dependencies include `tqdm` for CLI progress and `customtkinter` for the GUI).*

---

## 💻 Usage

### 🖥️ Modern Desktop GUI (Recommended)
If you prefer a visual interface, simply run:
```bash
python gui.py
```
This opens a modern desktop window where you can:
- Browse and select your input/output folders visually.
- Toggle options to delete original files or overwrite existing `.mp4`s.
- Press `Enter` to start, and watch the live progress bar.

### ⌨️ Command Line Interface (CLI)
Basic usage requires only the target folder path:
```bash
python convert.py /path/to/videos
```

#### CLI Options
| Flag | Description |
|------|-------------|
| `folder_path` | **(Required)** The root directory to scan for `.mov` files. |
| `--output <path>` | Specifies a custom directory to save converted `.mp4` files. |
| `--delete-original`| Deletes the original `.mov` files after successful conversion. |
| `--overwrite` | Forces FFmpeg to overwrite existing `.mp4` files. |
| `--verbose` | Enables debug-level logging output in the console. |

#### CLI Examples
*Convert in place:*
```bash
python convert.py ./videos
```
*Save to a new directory and delete the original `.mov` files:*
```bash
python convert.py ./videos --output ./converted_videos --delete-original
```
*Force overwrite existing files with verbose logging:*
```bash
python convert.py ./videos --overwrite --verbose
```

---

## 🛠️ Troubleshooting

- **`FFmpeg Missing` Error:**
  Ensure FFmpeg is installed correctly. Run `ffmpeg -version` in your terminal. If it's not recognized, you must add FFmpeg to your system's PATH environment variable.
- **Permission Errors:**
  Ensure you have read/write access to both the source and destination folders.
- **System Slowdown:**
  Video conversion is highly CPU-intensive. The tool intelligently limits threads to half your available CPU cores to prevent completely freezing your system, but high CPU usage is expected.

---

## 🧪 Running Tests

Unit tests are provided for core functionalities. From the root directory, run:
```bash
python -m unittest discover tests
```
