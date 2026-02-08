import argparse
import sys
import logging
from pathlib import Path
from openai import OpenAI
from clipper_core import AutoClipperCore
from config.config_manager import ConfigManager
from utils.helpers import get_app_dir, get_ffmpeg_path, get_ytdlp_path

# Setup basic logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="YT Short Clipper CLI - Headless Mode"
    )
    parser.add_argument("--url", required=True, help="YouTube video URL")
    parser.add_argument(
        "--num_clips", type=int, default=5, help="Number of clips to generate"
    )
    parser.add_argument(
        "--no_captions", action="store_true", help="Disable captions"
    )
    parser.add_argument(
        "--no_hook", action="store_true", help="Disable hook generation"
    )
    parser.add_argument(
        "--lang", default="id", help="Subtitle language (default: id)"
    )
    parser.add_argument("--output", help="Output directory")

    args = parser.parse_args()

    app_dir = get_app_dir()
    config_file = app_dir / "config.json"
    output_dir = Path(args.output) if args.output else (app_dir / "output")

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load configuration
    config_manager = ConfigManager(config_file, output_dir)
    config = (
        config_manager.get_all()
        if hasattr(config_manager, "get_all")
        else config_manager.config
    )

    # Setup core
    api_key = config.get("api_key", "")
    base_url = config.get("base_url", "https://api.openai.com/v1")
    model = config.get("model", "gpt-4.1")

    # Relax API key check for local providers in CLI
    is_local = (
        "localhost" in base_url
        or "11434" in base_url
        or "host.docker.internal" in base_url
    )
    if not api_key and is_local:
        api_key = "ollama"

    client = None
    if api_key:
        client = OpenAI(api_key=api_key, base_url=base_url)

    def log_cb(msg):
        logger.info(msg)

    def progress_cb(p):
        if p is not None:
            sys.stdout.write(
                f"\rProgress: [{'=' * int(p * 20):<20}] {p*100:.1f}%"
            )
            sys.stdout.flush()
            if p >= 1.0:
                print()

    core = AutoClipperCore(
        client=client,
        ffmpeg_path=get_ffmpeg_path(),
        ytdlp_path=get_ytdlp_path(),
        output_dir=str(output_dir),
        model=model,
        ai_providers=config.get("ai_providers"),
        subtitle_language=args.lang,
        log_callback=log_cb,
        progress_callback=lambda s, p=None: progress_cb(p),
    )

    try:
        logger.info(f"Starting processing for URL: {args.url}")
        core.process(
            args.url,
            num_clips=args.num_clips,
            add_captions=not args.no_captions,
            add_hook=not args.no_hook,
        )
        logger.info("Processing complete!")
    except Exception as e:
        logger.error(f"Error during processing: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
