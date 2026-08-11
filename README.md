# 🎬 MOV2MP4

A fast, simple batch MOV → MP4 converter powered by FFmpeg.

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![FFmpeg](https://img.shields.io/badge/Powered%20by-FFmpeg-green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)
![Status](https://img.shields.io/badge/Status-Stable-success)

> Screenshots coming soon.

MOV2MP4 is designed to automate the repetitive task of converting `.mov` files to `.mp4` formats. By discovering files recursively and processing them in parallel using an underlying FFmpeg engine, it handles heavy workloads effortlessly while keeping original directory structures intact.

Whether you prefer the precision of a command-line interface or the simplicity of a modern desktop application, MOV2MP4 offers a seamless, reliable experience without unnecessary complexity.

---

## ✨ Features

### Desktop GUI
- Modern macOS-inspired interface
- Drag & drop
- File/folder selection
- Conversion queue
- Per-file status
- Batch conversion
- Output destination selection
- Cancellation
- Responsive UI

### Conversion
- MOV → MP4
- FFmpeg powered
- Recursive folder scanning
- Batch processing
- Existing directory structure preservation
- Overwrite control
- Optional source deletion

### CLI
- Folder-based conversion
- Custom output directory
- Delete-original option
- Overwrite option
- Verbose logging

### Reliability
- Error handling
- Conversion status
- Logging
- Threaded processing
- Tests

---

## 📸 Screenshots

> Screenshots coming soon.

## 🎥 Demo

> Demo coming soon.

---

## 🏗️ How It Works

```text
MOV files
   ↓
File discovery
   ↓
Conversion queue
   ↓
FFmpeg processing
   ↓
MP4 output
   ↓
Status / logs
```

---

## 📦 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/MaybeSomeone-arc18/mov2mp4.git
cd mov2mp4
```

### 2. Set Up Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Install FFmpeg
FFmpeg must be installed and available in your system PATH.

**macOS**
```bash
brew install ffmpeg
```

**Ubuntu / Debian**
```bash
sudo apt install ffmpeg
```

**Windows**
```bash
winget install ffmpeg
```

Verify installation:
```bash
ffmpeg -version
```

---

## 🖥️ GUI Usage

1. Launch the application:
```bash
python gui.py
```

2. Add MOV files by:
   - dragging them into the drop zone
   - using Browse Files
   - selecting a folder

3. Review the conversion queue.
4. Choose the output destination.
5. Configure optional settings:
   - overwrite existing files
   - delete originals
6. Start conversion.
7. Monitor per-file and overall conversion status.
8. Cancel safely if needed.
9. Open the output folder after completion.

---

## ⌨️ CLI Usage

Convert all `.mov` files found inside a folder:
```bash
python convert.py ./videos
```

Convert to a Custom Output Folder:
```bash
python convert.py ./videos --output ./converted
```

Delete Original Files After Conversion:
```bash
python convert.py ./videos --delete-original
```

Force Overwrite Existing Files:
```bash
python convert.py ./videos --overwrite
```

Enable Verbose Logging:
```bash
python convert.py ./videos --verbose
```

### Command Reference

| Argument | Description |
|----------|-------------|
| `folder_path` | Root folder to scan for `.mov` files |
| `--output` | Custom output directory |
| `--delete-original` | Delete source files after successful conversion |
| `--overwrite` | Overwrite existing MP4 files |
| `--verbose` | Enable detailed debug logs |

---

## 📂 Example

Folder structure is preserved automatically.

**Input:**
```text
Videos/
├── Vacation/
│   ├── beach.mov
│   └── sunset.mov
└── Family/
    └── birthday.mov
```

**Output:**
```text
Converted/
├── Vacation/
│   ├── beach.mp4
│   └── sunset.mp4
└── Family/
    └── birthday.mp4
```

---

## 🏛️ Architecture

```text
          GUI                      CLI
           │                        │
 ┌─────────┴────────┐      ┌────────┴────────┐
 │ File selection   │      │ Args parsing    │
 │ Conversion queue │      │ Command flow    │
 │ Status updates   │      │ Verbose logging │
 └─────────┬────────┘      └────────┬────────┘
           │                        │
           ▼                        ▼
      ┌──────────────────────────────────┐
      │        Conversion Engine         │
      └────────────────┬─────────────────┘
                       ▼
      ┌──────────────────────────────────┐
      │              FFmpeg              │
      └────────────────┬─────────────────┘
                       ▼
      ┌──────────────────────────────────┐
      │            MP4 output            │
      └──────────────────────────────────┘
```

Both the GUI and CLI share the exact same underlying multithreaded Conversion Engine, ensuring that behavior, error handling, and reliability are consistent regardless of how you choose to use the tool.

---

## 🧪 Testing

Run all unit tests:
```bash
python -m unittest discover tests
```

Tests cover the core conversion logic, path resolution, CLI flags, FFmpeg integration, subprocess mocking, and file deletion safeguards.

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

### Permission Errors
Make sure you have:
- Read access to source folders
- Write access to output folders

### Drag and Drop Not Working
Ensure `tkinterdnd2` is correctly installed via `requirements.txt`. It is required for the OS-native drag-and-drop integration in the GUI.

---

## 📈 Why MOV2MP4?

MOV2MP4 is intentionally focused on one job:

Convert MOV files to MP4 quickly, in batches, without unnecessary complexity.

---

## ⚙️ Tech Stack

- Python
- FFmpeg
- CustomTkinter
- tkinterdnd2
- unittest

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a new feature branch
3. Commit your changes
4. Push your branch
5. Open a Pull Request

---

[GitHub Repository](https://github.com/MaybeSomeone-arc18/mov2mp4)
