# 🎬 MOV2MP4

> Turn MOV files into MP4 locally on your Mac or Windows PC—fast, private, and simple.

Made for editors, creators, and anyone who wants their videos converted without dealing with file limits, cloud uploads, or complicated settings.

---

## 📥 Download

### Windows

[**Download MOV2MP4 for Windows (x64)**](https://github.com/MaybeSomeone-arc18/mov2mp4/releases/tag/v0.1.0-windows)

*Works on Windows 10 and 11 (64-bit).*

### macOS

[**Download MOV2MP4 for Mac (Apple Silicon)**](https://github.com/MaybeSomeone-arc18/mov2mp4/releases/tag/v0.1.0-macos)

*Works on Apple Silicon Macs: M1, M2, M3, M4 and newer.*

---

## 🚀 First Time Setup

### Windows

You don't need to install Python, FFmpeg, Command Prompt/PowerShell tools, or pip packages. Everything is bundled into a single installer.

1. **Download the installer** — Download **`MOV2MP4-Setup.exe`**.
2. **Run the installer** — Double-click **`MOV2MP4-Setup.exe`** and follow the steps.
3. **Open MOV2MP4** — Open **MOV2MP4** from your **Start Menu** or **Desktop** shortcut.

#### ⚠️ If Windows Blocks the Installer

Because this is an unsigned project, Windows Defender SmartScreen might show a warning ("Unknown publisher"):

1. Click **More info**.
2. Click **Run anyway**.

---

### macOS

macOS is going to make the first launch slightly annoying.

I haven't paid for Apple's developer program yet, so macOS will probably complain that it can't verify the app. Don't worry—the app is completely fine, and you don't need to install Python, FFmpeg, Homebrew, or anything else.

### 1. Download & open the DMG
Download **`MOV2MP4-macOS-arm64.dmg`** and double-click to open it.

### 2. Move MOV2MP4 to Applications
Drag the **MOV2MP4** app into your **Applications** folder.

### 3. Open MOV2MP4
Go to **Applications → MOV2MP4** and double-click it. If it opens, you're all set! 🎉

---

## ⚠️ If macOS Blocks the App

If macOS displays a message saying it can't open or verify MOV2MP4:

1. Open **System Settings**.
2. Go to **Privacy & Security**.
3. Scroll down until you see the message about MOV2MP4 being blocked.
4. Click **Open Anyway** → then click **Open**.
5. Open **MOV2MP4** again.

### Still not opening?

There is a small helper included inside the downloaded DMG called **`Launch MOV2MP4`**.

1. Open the original DMG again.
2. Double-click **`Launch MOV2MP4.command`**.
3. If macOS blocks the launcher too, go back to **System Settings → Privacy & Security → Open Anyway** and then open the launcher again.

The launcher will clear the macOS security restriction and start MOV2MP4 for you. You only have to do this once.

### Advanced troubleshooting (Optional)

If you're comfortable with Terminal, you can clear the download restriction directly:

```bash
xattr -dr com.apple.quarantine "/Applications/MOV2MP4.app"
```

---

## 🎬 Using MOV2MP4

Once the app opens:

1. **Add your videos** — Drag your `.mov` files or folders directly into the app. You can add multiple files at once.
2. **Choose where your MP4s go** — Click **Browse Folder** to select where you want your converted videos saved.
3. **Convert** — Click **Start Conversion**.

Your MOV files stay on your computer. Nothing is ever uploaded anywhere.

### Useful Options

- **Batch conversion** — Convert queues of multiple videos at once.
- **Output Destination** — Save converted MP4s anywhere you choose.
- **Overwrite existing files** — Re-convert and overwrite existing MP4 files if needed.
- **Delete Original** — Automatically remove source MOV files after successful conversion. *(Be careful with this setting! Only turn it on if you actually want the original MOV files removed.)*
- **Cancel anytime** — Stop active conversions safely without corrupting files.

---

## 🛠️ For Developers & Power Users

MOV2MP4 runs on a unified multithreaded Python conversion engine powered by an embedded FFmpeg binary.

### Local Setup & Testing

```bash
# Clone repository
git clone https://github.com/MaybeSomeone-arc18/mov2mp4.git
cd mov2mp4

# Set up virtual environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run CLI
python convert.py ./videos --output ./converted

# Run unit tests
python3 -m unittest discover tests

# Build macOS DMG
./build_macos.sh
```

---

[GitHub Repository](https://github.com/MaybeSomeone-arc18/mov2mp4)
