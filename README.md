# 🎬 MOV2MP4

> A simple batch MOV → MP4 converter for video creators and editors.

MOV2MP4 converts `.mov` files to `.mp4` format locally on your computer. Drop your files in, choose where they go, and convert whole queues of video files without cloud uploads, file limits, or extra complexity.

---

## 📥 Download

### macOS

[**Download MOV2MP4 for Mac (Apple Silicon)**](https://github.com/MaybeSomeone-arc18/mov2mp4/releases/latest)

*For Apple Silicon Macs (M1, M2, M3, M4 and newer).*

> Windows version coming soon.

---

## 🚀 Get started

1. **Download** `MOV2MP4-macOS-arm64.dmg`.
2. **Drag** **MOV2MP4** into your **Applications** folder.
3. **Open** MOV2MP4.

---

## ⚠️ First launch on macOS

Because MOV2MP4 is an early preview build and is not notarized by Apple yet, macOS may ask you to approve it the first time you open it.

### If macOS gives you an "Open Anyway" option
Choose **Open Anyway → Open**.

### If macOS only shows "Move to Trash" or "Done"
1. Open **System Settings**.
2. Go to **Privacy & Security**.
3. Scroll down to the **Security** section.
4. Click **Open Anyway** next to MOV2MP4.
5. Confirm by clicking **Open**.

### Additional Fallback — Launch MOV2MP4 Launcher
If the normal app launch still does not work after the macOS approval flow, use the included **`Launch MOV2MP4.command`** helper inside the DMG:
1. Right-click (or Control-click) `Launch MOV2MP4.command`.
2. Select **Open**.
3. Confirm by clicking **Open**.

*(If macOS blocks the launcher too, repeat the **System Settings → Privacy & Security → Open Anyway** approval for the launcher.)*

### Advanced troubleshooting
*(Optional — for technical users only)*

To clear the macOS download restriction manually via Terminal:

```bash
xattr -dr com.apple.quarantine "/Applications/MOV2MP4.app"
```

---

## ✨ Features

- **Drag & Drop** — Drop MOV files or entire folder trees directly into the window.
- **Batch Processing** — Convert multiple videos simultaneously with multithreaded performance.
- **Folder Preservation** — Automatically preserves original nested directory structures.
- **Local & Private** — 100% offline conversion powered by an embedded FFmpeg engine.
- **Full Control** — Optional auto-overwrite and post-conversion source deletion.
- **Safe Cancellation** — Stop active batch conversions gracefully at any time.

---

## 💻 Usage

### Desktop Application
1. Add MOV files by dragging them into the drop zone or clicking **Browse Files** / **Browse Folder**.
2. Choose your output folder.
3. Configure optional settings *(Overwrite existing files / Delete originals after conversion)*.
4. Click **Start Conversion**.

### Command Line Interface (CLI)

```bash
# Convert a folder
python convert.py ./videos

# Choose an output folder
python convert.py ./videos --output ./converted

# Overwrite existing MP4 files
python convert.py ./videos --overwrite

# Delete original MOV files after successful conversion
python convert.py ./videos --delete-original
```

**Available flags:**
- `--output` — Custom output directory
- `--overwrite` — Overwrite existing MP4 files
- `--delete-original` — Delete source MOV files after successful conversion
- `--verbose` — Enable detailed debug logs

---

## 🏗️ Architecture & Development

MOV2MP4 shares a unified multithreaded Conversion Engine across both the Desktop GUI and CLI.

```text
  GUI / CLI  ──►  Conversion Engine  ──►  FFmpeg  ──►  MP4 Output
```

### Local Setup & Testing

```bash
# Clone repository
git clone https://github.com/MaybeSomeone-arc18/mov2mp4.git
cd mov2mp4

# Set up virtual environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run automated unit tests
python3 -m unittest discover tests

# Build macOS DMG
./build_macos.sh
```

---

[GitHub Repository](https://github.com/MaybeSomeone-arc18/mov2mp4)
