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
- Open your browser at **http://localhost:8501**.
- The web UI will guide you through URL input and processing.
- Your results will be saved in the local `output/` folder.

---

## 🌐 Option 2: Streamlit Web UI (Local)

Run the web interface directly on your machine without Docker.

### 1. Prerequisites
- Python 3.10+
- FFmpeg and Deno installed on your system.

### 2. Setup
```bash
pip install -r requirements.txt
```

### 3. Startup
```bash
streamlit run streamlit_app.py
```
This will automatically open the app in your default browser.

---

## 💻 Option 3: Command Line Interface (CLI)

Best for automation and batch processing.

### 1. Usage
```bash
python cli_app.py --url "YOUTUBE_URL" --num_clips 5
```

### 2. Arguments
| Argument | Default | Description |
|----------|---------|-------------|
| `--url` | (Required) | YouTube video URL |
| `--num_clips` | 5 | Number of clips to generate |
| `--no_captions` | False | Skip caption generation |
| `--no_hook` | False | Skip hook text generation |
| `--lang` | id | Subtitle language |

---

## ⚙️ Shared Requirements

Regardless of how you run the app, ensure you have:
1. **cookies.txt**: Required for authorized YouTube access. Export it using the browser extension 'Get cookies.txt LOCALLY' and place it in the project root or upload via Web UI.
2. **AI API Key**: Configure your provider (OpenAI, Gemini, Ollama, etc.) in the app settings.

> [!TIP]
> **Using Local AI (Ollama)**: Use `http://host.docker.internal:11434/v1` as the Base URL in settings when running via Docker.
