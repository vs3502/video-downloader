#!/usr/bin/env python3
"""
╔══════════════════════════════════════════╗
║       Multi-Platform Video Downloader    ║
║  YouTube • X (Twitter) • TikTok • Reddit ║
╚══════════════════════════════════════════╝
Requires: pip install yt-dlp
Optional: ffmpeg (for merging high-quality video+audio)
"""

import subprocess
import sys
import os
import re


# ─────────────────────────────────────────────
#  PLATFORM CONFIG
# ─────────────────────────────────────────────

PLATFORMS = {
    "1": {
        "name": "YouTube",
        "icon": "▶️ ",
        "color": "\033[91m",   # red
        "domains": ["youtube.com", "youtu.be"],
        "supports_quality": True,
        "supports_audio": True,
    },
    "2": {
        "name": "X (Twitter)",
        "icon": "🐦",
        "color": "\033[97m",   # white
        "domains": ["twitter.com", "x.com"],
        "supports_quality": False,
        "supports_audio": False,
    },
    "3": {
        "name": "TikTok",
        "icon": "🎵",
        "color": "\033[96m",   # cyan
        "domains": ["tiktok.com", "vm.tiktok.com"],
        "supports_quality": False,
        "supports_audio": False,
    },
    "4": {
        "name": "Reddit",
        "icon": "🤖",
        "color": "\033[93m",   # yellow/orange
        "domains": ["reddit.com", "v.redd.it", "redd.it"],
        "supports_quality": False,
        "supports_audio": False,
    },
}

# ANSI color codes
RESET  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
GREEN  = "\033[92m"
CYAN   = "\033[96m"
RED    = "\033[91m"
YELLOW = "\033[93m"
WHITE  = "\033[97m"


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────

def clear_line():
    print("\r" + " " * 80 + "\r", end="", flush=True)


def banner():
    print(f"""
{CYAN}{BOLD}
  ╔══════════════════════════════════════════════╗
  ║       MULTI-PLATFORM VIDEO DOWNLOADER        ║
  ║     YouTube  •  X  •  TikTok  •  Reddit      ║
  ╚══════════════════════════════════════════════╝
{RESET}""")


def install_ytdlp():
    try:
        import yt_dlp  # noqa: F401
    except ImportError:
        print(f"{YELLOW}📦 Installing yt-dlp...{RESET}")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "yt-dlp"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print(f"{GREEN}✅ yt-dlp installed!\n{RESET}")


def detect_platform(url):
    """Auto-detect platform from URL."""
    url_lower = url.lower()
    for key, info in PLATFORMS.items():
        for domain in info["domains"]:
            if domain in url_lower:
                return key
    return None


def progress_hook(d):
    if d["status"] == "downloading":
        percent = d.get("_percent_str", "??%").strip()
        speed   = d.get("_speed_str",   "??").strip()
        eta     = d.get("_eta_str",     "??").strip()
        bar_len = 30
        try:
            pct_val = float(percent.replace("%", ""))
            filled  = int(bar_len * pct_val / 100)
        except Exception:
            filled = 0
        bar = f"{GREEN}{'█' * filled}{DIM}{'░' * (bar_len - filled)}{RESET}"
        print(
            f"\r  {bar} {BOLD}{percent}{RESET}  {CYAN}{speed}{RESET}  ETA {eta}   ",
            end="",
            flush=True,
        )
    elif d["status"] == "finished":
        print(f"\n{GREEN}  ✅ File ready — processing...{RESET}")


# ─────────────────────────────────────────────
#  VIDEO INFO & FORMATS
# ─────────────────────────────────────────────

def get_info(url):
    import yt_dlp
    opts = {"quiet": True, "no_warnings": True}
    with yt_dlp.YoutubeDL(opts) as ydl:
        return ydl.extract_info(url, download=False)


def list_qualities(info):
    """Return sorted list of (label, height) tuples."""
    seen   = {}
    for f in info.get("formats", []):
        h = f.get("height")
        if h and f.get("vcodec", "none") != "none":
            seen[h] = f"{h}p"
    return sorted(seen.items(), reverse=True)   # [(1080, '1080p'), ...]


# ─────────────────────────────────────────────
#  DOWNLOAD
# ─────────────────────────────────────────────

def build_ydl_opts(platform_key, quality, audio_only, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    base_out = os.path.join(output_dir, "%(title)s.%(ext)s")

    # --- Audio only (YouTube) ---
    if audio_only:
        return {
            "format": "bestaudio/best",
            "outtmpl": base_out,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
            "progress_hooks": [progress_hook],
            "quiet": True,
            "no_warnings": True,
        }

    # --- YouTube with quality ---
    if platform_key == "1" and quality:
        if quality == "best":
            fmt = "bestvideo+bestaudio/best"
        else:
            h = quality.replace("p", "")
            fmt = f"bestvideo[height<={h}]+bestaudio/best[height<={h}]"
        return {
            "format": fmt,
            "outtmpl": base_out,
            "merge_output_format": "mp4",
            "progress_hooks": [progress_hook],
            "quiet": True,
            "no_warnings": True,
        }

    # --- X (Twitter) ---
    if platform_key == "2":
        return {
            "format": "best[ext=mp4]/best",
            "outtmpl": base_out,
            "progress_hooks": [progress_hook],
            "quiet": True,
            "no_warnings": True,
        }

    # --- TikTok ---
    if platform_key == "3":
        return {
            "format": "best",
            "outtmpl": base_out,
            "progress_hooks": [progress_hook],
            # Remove TikTok watermark when possible
            "postprocessor_args": [],
            "quiet": True,
            "no_warnings": True,
        }

    # --- Reddit ---
    if platform_key == "4":
        return {
            "format": "bestvideo+bestaudio/best",
            "outtmpl": base_out,
            "merge_output_format": "mp4",
            "progress_hooks": [progress_hook],
            "quiet": True,
            "no_warnings": True,
        }

    # Fallback
    return {
        "format": "best",
        "outtmpl": base_out,
        "progress_hooks": [progress_hook],
        "quiet": True,
        "no_warnings": True,
    }


def download(url, platform_key, quality=None, audio_only=False, output_dir=None):
    import yt_dlp
    opts = build_ydl_opts(platform_key, quality, audio_only, output_dir)
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])


# ─────────────────────────────────────────────
#  UI FLOWS
# ─────────────────────────────────────────────

def choose_platform():
    print(f"{BOLD}  Select a platform:{RESET}\n")
    for key, p in PLATFORMS.items():
        color = p["color"]
        print(f"    {color}{BOLD}[{key}]{RESET}  {p['icon']}  {color}{p['name']}{RESET}")
    print()

    while True:
        choice = input("  Enter number (1-4): ").strip()
        if choice in PLATFORMS:
            return choice
        print(f"  {RED}Invalid choice. Please enter 1, 2, 3, or 4.{RESET}")


def choose_download_type():
    print(f"\n{BOLD}  Download type:{RESET}")
    print(f"    {GREEN}[1]{RESET}  🎬  Video (MP4)")
    print(f"    {GREEN}[2]{RESET}  🎵  Audio only (MP3)")
    print()
    while True:
        c = input("  Enter choice (1 or 2): ").strip()
        if c in ("1", "2"):
            return c == "2"
        print(f"  {RED}Please enter 1 or 2.{RESET}")


def choose_quality(qualities):
    print(f"\n{BOLD}  Available qualities:{RESET}\n")
    tags = {1080: f"{RED}🔥 Full HD{RESET}", 720: f"{YELLOW}⭐ HD{RESET}",
            480: f"{GREEN}👍 SD{RESET}", 360: f"{DIM}360p{RESET}"}

    for i, (h, label) in enumerate(qualities, 1):
        tag = ""
        for threshold, t in tags.items():
            if h >= threshold:
                tag = f"  {t}"
                break
        print(f"    {GREEN}[{i}]{RESET}  {label}{tag}")

    n = len(qualities)
    print(f"    {GREEN}[{n+1}]{RESET}  ⚡ Best available (auto)")
    print()

    while True:
        try:
            c = int(input("  Choose quality: ").strip())
            if 1 <= c <= n:
                return f"{qualities[c-1][0]}p"
            elif c == n + 1:
                return "best"
        except ValueError:
            pass
        print(f"  {RED}Invalid choice.{RESET}")


def choose_output_dir(platform_name):
    default = os.path.join(os.path.expanduser("~"), "Downloads", "VideoDownloader", platform_name)
    print(f"\n{BOLD}  Save location:{RESET}")
    print(f"  {DIM}Default: {default}{RESET}")
    d = input("  Press Enter to use default, or type a path: ").strip()
    return d if d else default


def show_video_info(info, platform):
    title    = info.get("title", "Unknown")[:60]
    uploader = info.get("uploader") or info.get("channel") or info.get("creator") or "Unknown"
    duration = info.get("duration", 0) or 0
    mins, secs = divmod(int(duration), 60)

    color = PLATFORMS[platform]["color"]
    print(f"\n  {color}{'─'*48}{RESET}")
    print(f"  {BOLD}📹 {title}{RESET}")
    print(f"  {DIM}👤 {uploader}   ⏱️  {mins}m {secs:02d}s{RESET}")
    print(f"  {color}{'─'*48}{RESET}\n")


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────

def main():
    banner()
    install_ytdlp()

    # ── Step 1: Platform ──
    platform_key = choose_platform()
    platform     = PLATFORMS[platform_key]
    color        = platform["color"]

    print(f"\n  {color}{BOLD}✔ {platform['name']} selected{RESET}\n")
    print(f"  {'─'*48}")

    # ── Step 2: URL ──
    url = input(f"\n  🔗 Paste {platform['name']} URL: ").strip()
    if not url:
        print(f"  {RED}❌ No URL provided. Exiting.{RESET}")
        sys.exit(1)

    # Auto-detect mismatch warning
    detected = detect_platform(url)
    if detected and detected != platform_key:
        wrong = PLATFORMS[detected]["name"]
        print(f"  {YELLOW}⚠️  This looks like a {wrong} link. Continuing anyway...{RESET}")

    # ── Step 3: Fetch info ──
    print(f"\n  {DIM}🔍 Fetching info...{RESET}")
    try:
        info = get_info(url)
    except Exception as e:
        print(f"  {RED}❌ Could not fetch video info:{RESET}")
        print(f"  {DIM}{e}{RESET}")
        print(f"\n  {YELLOW}💡 Tips:{RESET}")
        print(f"  • Make sure the URL is correct and the video is public")
        print(f"  • For X/Twitter, login may be required for some videos")
        print(f"  • Try updating yt-dlp: {CYAN}pip install -U yt-dlp{RESET}")
        sys.exit(1)

    show_video_info(info, platform_key)

    # ── Step 4: Options ──
    audio_only = False
    quality    = None

    if platform["supports_audio"]:
        audio_only = choose_download_type()

    if not audio_only and platform["supports_quality"]:
        qualities = list_qualities(info)
        if qualities:
            quality = choose_quality(qualities)
        else:
            print(f"  {YELLOW}⚠️  No quality data found — using best available.{RESET}")
            quality = "best"
    elif not audio_only:
        print(f"  {DIM}ℹ️  Downloading best available quality for {platform['name']}.{RESET}")

    # ── Step 5: Output dir ──
    output_dir = choose_output_dir(platform["name"])

    # ── Step 6: Download ──
    print(f"\n  {color}{'═'*48}{RESET}")
    if audio_only:
        print(f"  {BOLD}🎵 Downloading audio as MP3...{RESET}")
    else:
        q_label = quality or "best"
        print(f"  {BOLD}🎬 Downloading {platform['name']} video ({q_label})...{RESET}")
    print(f"  {color}{'═'*48}{RESET}\n")

    try:
        download(url, platform_key, quality=quality, audio_only=audio_only, output_dir=output_dir)
    except Exception as e:
        err = str(e)
        print(f"\n  {RED}❌ Download failed:{RESET}")
        print(f"  {DIM}{err}{RESET}")

        print(f"\n  {YELLOW}💡 Troubleshooting:{RESET}")
        if "ffmpeg" in err.lower():
            print(f"  • Install ffmpeg → https://ffmpeg.org/download.html")
        elif "private" in err.lower() or "login" in err.lower():
            print(f"  • This video may be private or require login")
        elif "copyright" in err.lower():
            print(f"  • This video may be copyright-restricted in your region")
        else:
            print(f"  • Try updating yt-dlp: {CYAN}pip install -U yt-dlp{RESET}")
            print(f"  • Make sure the URL is correct and the video is public")
        sys.exit(1)

    # ── Done ──
    print(f"\n  {GREEN}{BOLD}🎉 Download complete!{RESET}")
    print(f"  {DIM}📁 Saved to: {output_dir}{RESET}")
    print(f"\n  {'─'*48}")

    again = input(f"\n  {BOLD}Download another? (y/n):{RESET} ").strip().lower()
    if again == "y":
        print()
        main()
    else:
        print(f"\n  {CYAN}Thanks for using Video Downloader! 🚀{RESET}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {YELLOW}⚡ Cancelled by user.{RESET}\n")
        sys.exit(0)