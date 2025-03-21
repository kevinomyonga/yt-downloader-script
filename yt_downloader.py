"""
Copyright (c) 2024 - 2025 Kevin Omyonga. All rights reserved.
"""
    
import os
import threading
from datetime import datetime
from yt_dlp import YoutubeDL

RESOLUTION = "1080"
FORMAT_SELECTION = f"bestvideo[height<={RESOLUTION}]+bestaudio/best[height<={RESOLUTION}]"  # Select 720p or lower
POSTPROCESSORS = [
    {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"},  # Ensure output format is MP4
    {"key": "FFmpegFixupM4a"},  # Ensure AAC audio compatibility
]
POSTPROCESSOR_ARGS = [
    "-vcodec", "libx264",  # Use H.264 video codec
    "-acodec", "aac",      # Use AAC audio codec
    "-strict", "experimental",
]


def log_message(message, log_file):
    """Logs a message to the log file and prints it to the console."""
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(log_file, "a") as f:
        f.write(f"{timestamp} {message}\n")
    print(message)


def is_video_downloaded(video_title, download_path):
    """Checks if the video with the given title is already downloaded."""
    return any(
        os.path.exists(os.path.join(download_path, f"{video_title}.{ext}"))
        for ext in ["mp4", "mkv", "webm"]
    )


def get_ydl_options(download_path):
    """Returns the common YouTubeDL options."""
    return {
        "format": FORMAT_SELECTION,
        "outtmpl": os.path.join(download_path, "%(title)s.%(ext)s"),
        "merge_output_format": "mp4",
        "ignoreerrors": True,
        "postprocessors": POSTPROCESSORS,
        "postprocessor_args": POSTPROCESSOR_ARGS,
    }


def download_item(item_url, download_path, log_file, is_playlist=False):
    """Downloads a video or playlist."""
    try:
        ydl_opts = get_ydl_options(download_path)
        with YoutubeDL(ydl_opts) as ydl:
            if is_playlist:
                log_message(f"Processing playlist: {item_url}", log_file)
                result = ydl.extract_info(item_url, download=True)
                for entry in (result["entries"] or []):
                    if entry is None:
                        log_message("Skipping unavailable video.", log_file)
                        continue
                    process_video_entry(entry, download_path, log_file, ydl)
            else:
                log_message(f"Processing video: {item_url}", log_file)
                info_dict = ydl.extract_info(item_url, download=False)
                process_video_entry(info_dict, download_path, log_file, ydl)
    except Exception as e:
        log_message(f"Failed to process {'playlist' if is_playlist else 'video'}: {item_url}\nError: {e}", log_file)


def process_video_entry(entry, download_path, log_file, ydl):
    """Processes a single video entry."""
    video_title = entry["title"]
    video_url = entry["webpage_url"]
    if is_video_downloaded(video_title, download_path):
        log_message(f"Skipping already downloaded video: {video_title}", log_file)
    else:
        log_message(f"Downloading video: {video_title}", log_file)
        ydl.download([video_url])
        log_message(f"Downloaded video: {video_title}", log_file)


def main():
    url = input("Enter the YouTube video or playlist URL: ").strip()
    download_path = "./downloads"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"logs/log_{timestamp}.txt"

    log_message("Script started.", log_file)
    is_playlist = "list=" in url

    download_thread = threading.Thread(
        target=download_item,
        args=(url, download_path, log_file, is_playlist),
        daemon=True
    )

    download_thread.start()
    log_message("Download process started in a separate thread.", log_file)
    download_thread.join()
    log_message("Script finished.", log_file)


if __name__ == "__main__":
    main()
