import streamlit as st
import os
import sys
import json
import time
import threading
from pathlib import Path
from clipper_core import AutoClipperCore
from config.config_manager import ConfigManager
from utils.helpers import (
    get_app_dir,
    get_ffmpeg_path,
    get_ytdlp_path,
    extract_video_id,
)
from openai import OpenAI

# Page config
st.set_page_config(
    page_title="YT Short Clipper",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Constants
APP_DIR = get_app_dir()
CONFIG_FILE = APP_DIR / "config.json"
OUTPUT_DIR = APP_DIR / "output"
COOKIES_FILE = APP_DIR / "cookies.txt"

# Ensure directories exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Initialize Session State
if "processing" not in st.session_state:
    st.session_state.processing = False
if "logs" not in st.session_state:
    st.session_state.logs = []
if "progress" not in st.session_state:
    st.session_state.progress = 0.0
if "status" not in st.session_state:
    st.session_state.status = ""
if "cancelled" not in st.session_state:
    st.session_state.cancelled = False

# Load Config
config_manager = ConfigManager(CONFIG_FILE, OUTPUT_DIR)
config = config_manager.config

# Sidebar - Settings
with st.sidebar:
    st.title("⚙️ Settings")

    # API Settings
    st.subheader("AI API Configuration")
    api_key = st.text_input(
        "OpenAI API Key", value=config.get("api_key", ""), type="password"
    )
    base_url = st.text_input(
        "Base URL", value=config.get("base_url", "https://api.openai.com/v1")
    )
    model = st.text_input("Model", value=config.get("model", "gpt-4.1"))

    if st.button("Save Settings"):
        config["api_key"] = api_key
        config["base_url"] = base_url
        config["model"] = model
        config_manager.save()
        st.success("Settings saved!")

    st.divider()

    # Cookies Status
    st.subheader("🍪 Cookies")
    if COOKIES_FILE.exists():
        st.success("cookies.txt loaded")
    else:
        st.warning("cookies.txt missing")
        uploaded_file = st.file_uploader("Upload cookies.txt", type="txt")
        if uploaded_file is not None:
            with open(COOKIES_FILE, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.rerun()

# Main UI
st.title("🎬 YT Short Clipper")
st.markdown(
    "Transform long-form YouTube videos into engaging shorts using AI."
)

col1, col2 = st.columns([2, 1])

with col1:
    url = st.text_input(
        "YouTube URL", placeholder="https://www.youtube.com/watch?v=..."
    )
    num_clips = st.slider("Number of Clips", 1, 10, 5)

    with st.expander("Advanced Options"):
        lang = st.selectbox(
            "Subtitle Language", ["id", "en", "es", "fr"], index=0
        )
        c1, c2 = st.columns(2)
        with c1:
            add_captions = st.checkbox("Add Captions", value=True)
        with c2:
            add_hook = st.checkbox("Add Hook Text", value=True)

    if st.button(
        "🚀 Start Processing", disabled=st.session_state.processing or not url
    ):
        st.session_state.processing = True
        st.session_state.logs = []
        st.session_state.progress = 0.0
        st.session_state.status = "Initializing..."
        st.session_state.cancelled = False
        st.rerun()

# Processing UI
if st.session_state.processing:
    st.divider()
    st.subheader("⏳ Processing...")

    progress_bar = st.progress(st.session_state.progress)
    status_text = st.empty()
    log_area = st.empty()

    if st.button("🛑 Cancel"):
        st.session_state.cancelled = True
        st.warning("Cancellation requested...")

    # Log/Progress Callbacks
    def log_callback(msg):
        st.session_state.logs.append(msg)
        # Keep logs limited
        if len(st.session_state.logs) > 100:
            st.session_state.logs.pop(0)

    def progress_callback(status, progress=None):
        st.session_state.status = status
        if progress is not None:
            st.session_state.progress = progress

    def cancel_check():
        return st.session_state.cancelled

    # Wrapper for thread
    def run_clipper():
        try:
            client = OpenAI(api_key=api_key, base_url=base_url)
            core = AutoClipperCore(
                client=client,
                ffmpeg_path=get_ffmpeg_path(),
                ytdlp_path=get_ytdlp_path(),
                output_dir=str(OUTPUT_DIR),
                model=model,
                ai_providers=config.get("ai_providers"),
                subtitle_language=lang,
                log_callback=log_callback,
                progress_callback=progress_callback,
                cancel_check=cancel_check,
            )

            core.process(
                url,
                num_clips=num_clips,
                add_captions=add_captions,
                add_hook=add_hook,
            )
            st.session_state.status = "Complete!"
            st.session_state.progress = 1.0
        except Exception as e:
            st.error(f"Error: {e}")
        finally:
            st.session_state.processing = False

    # Start thread if not already running a background task (simple state)
    if (
        "thread" not in st.session_state
        or not st.session_state.thread.is_alive()
    ):
        thread = threading.Thread(target=run_clipper)
        st.session_state.thread = thread
        thread.start()

    # Dynamic UI Updates
    while st.session_state.processing:
        progress_bar.progress(st.session_state.progress)
        status_text.text(f"Status: {st.session_state.status}")
        log_area.text_area(
            "Logs", value="\n".join(st.session_state.logs), height=200
        )
        time.sleep(0.5)

    st.session_state.processing = False
    st.success("Processing finished!")
    st.rerun()

# Results Gallery
st.divider()
st.subheader("📁 Results")

if OUTPUT_DIR.exists():
    # Find clip folders
    clip_folders = sorted(
        [
            d
            for d in OUTPUT_DIR.iterdir()
            if d.is_dir() and not d.name.startswith("_")
        ],
        reverse=True,
    )

    if not clip_folders:
        st.info("No clips found yet. Start processing to create some!")
    else:
        for folder in clip_folders[:5]:
            with st.container():
                data_file = folder / "data.json"
                video_file = folder / "master.mp4"

                if data_file.exists() and video_file.exists():
                    try:
                        with open(data_file, "r") as f:
                            data = json.load(f)

                        c1, c2 = st.columns([1, 2])
                        with c1:
                            st.video(str(video_file))
                        with c2:
                            st.write(f"**{data.get('title', 'Untitled')}**")
                            st.write(f"Hook: {data.get('hook_text', '')}")
                            st.write(
                                f"Duration: {data.get('duration_seconds', 0):.1f}s"
                            )
                            st.download_button(
                                "Download Clip",
                                open(video_file, "rb"),
                                file_name=f"{folder.name}.mp4",
                            )
                    except:
                        pass
                st.divider()
