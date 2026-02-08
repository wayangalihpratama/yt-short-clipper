# 🚀 Run Guide

This guide explains how to run **YT-Short-Clipper** in various modes: Docker, Streamlit Web UI, and Command Line Interface (CLI).

---

## 🐳 Option 1: Docker (Recommended)

Docker is the easiest way to run the app as it bundles all requirements (FFmpeg, Deno, Python dependencies) into a single container.

### 1. Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.

### 2. Startup
Run the following command in the project root:
```bash
docker compose up -d
```

### 3. Usage
1. Open your browser at **http://localhost:8501**.
2. **Configure AI**: Click the ⚙️ icon in the sidebar to enter your API key and base URL (e.g., for OpenAI or Ollama).
3. **Upload Cookies**: If needed, upload your `cookies.txt` via the sidebar.
4. **Process**: Enter a YouTube URL, adjust the number of clips, and click **🚀 Start Processing**.
5. **Monitor**: Watch the logs and progress bar in real-time.
6. **Results**: View and download finished clips from the gallery at the bottom.

---

## 🌐 Option 2: Streamlit Web UI (Local)

Run the web interface directly on your machine without Docker.

### 1. Prerequisites
- Python 3.10+
- FFmpeg and Deno installed on your system.

### 2. Setup & Startup
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

---

## 💻 Option 3: Command Line Interface (CLI)

Best for automation and batch processing.

### 1. Basic Usage
```bash
python cli_app.py --url "YOUTUBE_URL" --num_clips 5
```

### 2. Running CLI inside Docker
If you prefer using the CLI but want the Docker environment:
```bash
docker run --rm -v $(pwd)/output:/app/output --entrypoint python yt-short-clipper cli_app.py --url "URL" --num_clips 1
```

### 3. Arguments
| Argument | Default | Description |
|----------|---------|-------------|
| `--url` | (Required) | YouTube video URL |
| `--num_clips` | 5 | Number of clips to generate |
| `--no_captions` | False | Skip caption generation |
| `--no_hook` | False | Skip hook text generation |
| `--lang` | id | Subtitle language |

---

## ✅ Verification: Testing Your Setup

To quickly test if your installation (FFmpeg, Deno, etc.) is working correctly without using AI credits, run this "no-AI" test command:

**Local CLI:**
```bash
python cli_app.py --url "https://www.youtube.com/shorts/dQw4w9WgXcQ" --num_clips 1 --no_captions --no_hook
```

**Docker CLI:**
```bash
docker run --rm -v $(pwd)/output:/app/output --entrypoint python yt-short-clipper cli_app.py --url "https://www.youtube.com/shorts/dQw4w9WgXcQ" --num_clips 1 --no_captions --no_hook
```

---

## ⚙️ Shared Requirements

Regardless of how you run the app, ensure you have:
1. **cookies.txt**: Required for authorized YouTube access. Place it in the project root or upload via the Web UI sidebar.
2. **AI API Key**: Set your provider (OpenAI, Gemini, Ollama, etc.) in the app settings.

> [!TIP]
> **Using Local AI (Ollama)**: Use `http://host.docker.internal:11434/v1` as the Base URL in settings when running via Docker.
