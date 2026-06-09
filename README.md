# 🎬 MOV2MP4

> A fast, modern, and reliable batch video converter that transforms `.mov` files into `.mp4` using FFmpeg. Built with both a powerful Command Line Interface (CLI) and an intuitive Desktop GUI.

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![FFmpeg](https://img.shields.io/badge/Powered%20by-FFmpeg-green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success)

---

## ✨ Overview

MOV2MP4 is designed for creators, developers, editors, and anyone who regularly works with video files.

Instead of manually converting videos one at a time, MOV2MP4 automatically discovers `.mov` files, processes them in parallel, tracks progress in real time, and outputs optimized `.mp4` files while preserving your folder structure.

Whether you're converting a handful of videos or thousands of files spread across multiple directories, MOV2MP4 handles the workflow efficiently and safely.

---

## 🚀 Features

### 🎨 Modern Desktop GUI

A clean and responsive graphical interface built with `customtkinter`.

- Dark and light appearance modes
- Folder selection dialogs
- One-click conversion
- Real-time progress tracking
- User-friendly workflow

### ⚡ High Performance

Designed for speed.

- Multithreaded video processing
- Concurrent file conversion
- Optimized CPU utilization
- Efficient batch processing

### 📁 Smart File Management

- Recursive folder scanning
- Preserves original directory structure
- Supports custom output locations
- Automatically skips already converted files

### 🛡️ Safe Conversion

- Prevents accidental overwrites
- Optional overwrite mode
- Optional deletion of source files
- Robust error handling

### 📊 Detailed Logging

Every run is logged for transparency and debugging.

- Timestamped logs
- Success and failure reporting
- Debug mode support
- Conversion statistics

---

## 📸 Preview

### Desktop GUI

Add screenshots or GIFs here:

```text
┌─────────────────────────────┐
│         MOV2MP4             │
│                             │
│ Input Folder   [Browse]     │
│ Output Folder  [Browse]     │
│                             │
│ ████████████░░░░░░ 65%      │
│                             │
│ Converted: 52 / 80 files    │
│                             │
│       [ Start Convert ]     │
└─────────────────────────────┘
```

---

## 🏗️ How It Works

```text
Scan Folder
    │
    ▼
Find All .mov Files
    │
    ▼
Build Conversion Queue
    │
    ▼
Process Files Concurrently
    │
    ▼
Generate .mp4 Files
    │
    ▼
Update Progress & Logs
```

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/MaybeSomeone-arc18/mov2mp4.git
cd mov2mp4
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install FFmpeg

FFmpeg must be installed and available in your system PATH.

#### macOS

```bash
brew install ffmpeg
```

#### Ubuntu / Debian

```bash
sudo apt install ffmpeg
```

#### Windows

```bash
winget install ffmpeg
```

Verify installation:

```bash
ffmpeg -version
```

---

## 🖥️ GUI Usage

Launch the graphical application:

```bash
python gui.py
```

### GUI Features

- Select source folder
- Select destination folder
- Enable overwrite mode
- Delete originals after conversion
- View live progress updates
- Monitor conversion status

---

## ⌨️ CLI Usage

### Basic Conversion

Convert all `.mov` files found inside a folder:

```bash
python convert.py ./videos
```

### Convert to a Custom Output Folder

```bash
python convert.py ./videos --output ./converted
```

### Delete Original Files After Conversion

```bash
python convert.py ./videos --delete-original
```

### Force Overwrite Existing Files

```bash
python convert.py ./videos --overwrite
```

### Enable Verbose Logging

```bash
python convert.py ./videos --verbose
```

---

## 📚 Command Reference

| Argument | Description |
|----------|-------------|
| `folder_path` | Root folder to scan for `.mov` files |
| `--output` | Custom output directory |
| `--delete-original` | Delete source files after successful conversion |
| `--overwrite` | Overwrite existing MP4 files |
| `--verbose` | Enable detailed debug logs |

---

## 📂 Example

### Input

```text
Videos/
├── Vacation/
│   ├── beach.mov
│   └── sunset.mov
│
└── Family/
    └── birthday.mov
```

### Output

```text
Converted/
├── Vacation/
│   ├── beach.mp4
│   └── sunset.mp4
│
└── Family/
    └── birthday.mp4
```

Folder structure is preserved automatically.

---

## 🧪 Running Tests

Run all unit tests:

```bash
python -m unittest discover tests
```

---

## 🛠️ Troubleshooting

### FFmpeg Not Found

Check installation:

```bash
ffmpeg -version
```

If the command is not recognized:

- Install FFmpeg
- Ensure FFmpeg is added to PATH
- Restart your terminal

---

### Permission Errors

Make sure you have:

- Read access to source folders
- Write access to output folders

---

### High CPU Usage

Video conversion is CPU intensive.

MOV2MP4 automatically limits worker threads to avoid consuming all available system resources while maintaining fast performance.

---

## 📈 Why Use MOV2MP4?

| Feature | MOV2MP4 |
|----------|----------|
| Batch Conversion | ✅ |
| Recursive Scanning | ✅ |
| Folder Preservation | ✅ |
| GUI Support | ✅ |
| CLI Support | ✅ |
| Progress Tracking | ✅ |
| Multithreading | ✅ |
| Logging | ✅ |
| Cross Platform | ✅ |

---

## 🤝 Contributing

Contributions are welcome.

To contribute:

1. Fork the repository
2. Create a new feature branch
3. Commit your changes
4. Push your branch
5. Open a Pull Request

Bug reports, feature requests, and improvements are always appreciated.

---

## 🌟 Support

If you find this project useful:

- ⭐ Star the repository
- 🍴 Fork the project
- 🐛 Report bugs
- 🚀 Suggest improvements

---

<p align="center">
Built with ❤️ using Python and FFmpeg
</p>
