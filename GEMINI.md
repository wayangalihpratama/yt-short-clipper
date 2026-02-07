# GEMINI.md - Fork-Safe Enhanced Project Overview

## 🎬 Project Mission
**YT-Short-Clipper** is an automated pipeline designed to transform long-form YouTube videos into engaging short-form content (Shorts, Reels, TikTok) using AI. It handles downloading, highlight detection, portrait conversion, hook generation, and captioning.

## 🛠 Tech Stack
- **Language**: Python 3.10+
- **GUI Framework**: CustomTkinter
- **Video Processing**: FFmpeg
- **Computer Vision**: OpenCV, MediaPipe
- **AI Integration**:
  - GPT-4 (Highlights, Hook Text)
  - OpenAI Whisper (Captions)
  - OpenAI TTS (Voiceover)
  - Multiple providers supported via configuration (Google Gemini, Groq, etc.)
- **Utilities**: yt-dlp (Downloading)

## 🏗 Core Components
- `app.py`: Main entry point and GUI logic.
- `clipper_core.py`: Orchestrates the processing pipeline (download -> detect -> cut -> convert -> hooks -> captions).
- `youtube_uploader.py`: Handles uploading finished clips.
- `tiktok_uploader.py`: Placeholder for TikTok uploading logic.
- `config/`: Configuration management.
- `utils/`: Common utilities for video, text, and API handling.

## 📁 Key Directories
- `assets/`: UI assets (icons).
- `output/`: Generated clips and temporary files.
- `pages/`: GUI view components.
- `dialogs/`: GUI popup windows.

## 🎯 Development Goals
1. Improve speaker tracking accuracy.
2. Support more automated upload platforms.
3. Enhance caption styling and animation options.
4. Better handle large batch processing.
