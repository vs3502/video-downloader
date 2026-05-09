# 🎬 Multi-Platform Video Downloader

A simple and clean video downloader that supports **YouTube, X (Twitter), TikTok, and Reddit**.
Available as a **GUI app** for Windows and a **terminal app** for Android (Termux).

---

## ✨ Features

- 🖥️ Clean dark GUI interface (Windows)
- 📱 Terminal interface for Android (Termux)
- ▶️ YouTube — quality selection (1080p, 720p, 480p, 360p) + MP3 audio
- 🐦 X (Twitter) — download videos from tweets
- 🎵 TikTok — download videos
- 👽 Reddit — download videos
- ⚡ Auto-detects platform from URL
- 🔄 Auto-updater — always stays up to date
- 📁 Saves directly to your Downloads folder

---

## 📸 Screenshot

> GUI running on Windows

![GUI Screenshot](https://raw.githubusercontent.com/vs3502/video-downloader/main/screenshot.png)

---

## 📦 Installation

### 🖥️ Windows — GUI Version (Recommended)

**Option A — Just download the exe (easiest):**

1. Download `gui_downloader.exe` from this repo
2. Double-click to run
3. Done — no installation needed!

**Option B — Run from source:**

1. Make sure you have [Python](https://python.org) installed
2. Install dependencies:
```bash
pip install customtkinter yt-dlp
```
3. Install [ffmpeg](https://ffmpeg.org/download.html) for HD video
4. Install [Node.js](https://nodejs.org) for YouTube support
5. Run:
```bash
python gui_downloader.py
```

---

### 📱 Android — Termux Version

**Step 1 — Install Termux from F-Droid:**
```
https://f-droid.org/packages/com.termux/
```
> ⚠️ Do NOT install from Google Play Store — it's outdated

**Step 2 — Setup Termux:**
```bash
pkg update && pkg upgrade
pkg install python ffmpeg git
pip install yt-dlp
```

**Step 3 — Grant storage permission:**
```bash
termux-setup-storage
```
Allow the permission when prompted.

**Step 4 — Clone this repo:**
```bash
git clone https://github.com/vs3502/video-downloader.git
```

**Step 5 — Run:**
```bash
python ~/video-downloader/video_downloader.py
```

---

## 🚀 How to Use

### GUI (Windows)
1. Open `gui_downloader.exe`
2. Click the platform tab (YouTube, X, TikTok, Reddit)
3. Paste your video link
4. Choose quality (YouTube only)
5. Click **⬇ Download**
6. Find your video in `Downloads/VideoDownloader/`

### Terminal (Termux/PC)
1. Run `python video_downloader.py`
2. Choose platform (1-4)
3. Paste your video link
4. Choose quality
5. Press Enter to download

---

## 🌐 Supported Platforms

| Platform | Video | Audio (MP3) | Quality Selection |
|----------|-------|-------------|-------------------|
| ▶️ YouTube | ✅ | ✅ | ✅ 1080p → 360p |
| 🐦 X (Twitter) | ✅ | ❌ | ❌ Auto best |
| 🎵 TikTok | ✅ | ❌ | ❌ Auto best |
| 👽 Reddit | ✅ | ❌ | ❌ Auto best |

---

## ⚙️ Requirements

| Tool | Purpose | Required? |
|------|---------|-----------|
| [Python 3.8+](https://python.org) | Run the script | ✅ Yes (not needed for .exe) |
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) | Download engine | ✅ Yes |
| [ffmpeg](https://ffmpeg.org) | Merge HD video+audio | ⚠️ For 720p+ |
| [Node.js](https://nodejs.org) | YouTube JS support | ⚠️ Recommended |
| [customtkinter](https://github.com/TomSchimansky/CustomTkinter) | GUI library | ✅ GUI version only |

---

## 🔄 How to Update

**On PC (terminal):**
```bash
cd video-downloader
git pull
```

**On Termux:**
```bash
cd ~/video-downloader && git pull
```

The program also **auto-checks for updates** every time it launches and updates itself automatically.

---

## 🐛 Troubleshooting

| Problem | Fix |
|---------|-----|
| `ffmpeg not found` | Install ffmpeg from https://ffmpeg.org |
| `No module named yt_dlp` | Run `pip install yt-dlp` |
| Video is private | Only public videos can be downloaded |
| Download stuck at "Fetching info" | Install Node.js from https://nodejs.org |
| Permission denied (Termux) | Run `termux-setup-storage` and allow permission |
| yt-dlp stops working | Run `pip install -U yt-dlp` to update |
| GUI window doesn't open | Run `pip install customtkinter --upgrade` |

---

## 📁 Project Structure

```
video-downloader/
│
├── gui_downloader.exe      ← Windows GUI app (download this)
├── gui_downloader.py       ← GUI source code
├── video_downloader.py     ← Terminal version (Termux/PC)
├── install.bat             ← Windows auto-installer
└── version.txt             ← Version tracking for auto-updater
```

---

## 📜 License

MIT License — free to use, share, and modify.

---

## 👤 Author

Made by **vs3502**
GitHub: [github.com/vs3502](https://github.com/vs3502)

---

> ⚠️ **Disclaimer:** This tool is for personal use only.
> Please respect copyright laws and the terms of service of each platform.
> Only download videos you have permission to download.
