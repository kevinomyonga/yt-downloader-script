"""
Copyright (c) 2024 Kevin Omyonga. All rights reserved.
"""

import os
import threading
from datetime import datetime
from yt_dlp import YoutubeDL

def log_message(message, log_file):
    """Logs a message to the log file and prints it to the console."""
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(log_file, "a") as f:
        f.write(f"{timestamp} {message}\n")
    print(message)

def is_video_downloaded(video_title, download_path):
    """Checks if the video with the given title is already downloaded."""
    for ext in ["mp4", "mkv", "webm"]:
        if os.path.exists(os.path.join(download_path, f"{video_title}.{ext}")):
            return True
    return False

def download_video(video_url, download_path, log_file):
    """Downloads a single video."""
    try:
        ydl_opts = {
            "format": "best[height<=1080]",
            "outtmpl": os.path.join(download_path, "%(title)s.%(ext)s"),
            "ignoreerrors": True,  # Skip errors and continue downloading other videos
        }
        with YoutubeDL(ydl_opts) as ydl:
            log_message(f"Processing video: {video_url}", log_file)
            info_dict = ydl.extract_info(video_url, download=False)
            video_title = info_dict["title"]

            if is_video_downloaded(video_title, download_path):
                log_message(f"Skipping already downloaded video: {video_title}", log_file)
            else:
                ydl.download([video_url])
                log_message(f"Downloaded video: {video_title}", log_file)
    except Exception as e:
        log_message(f"Failed to download video: {video_url}\nError: {e}", log_file)

def download_playlist(playlist_url, download_path, log_file):
    """Downloads all videos in a playlist, skipping already downloaded ones."""
    try:
        ydl_opts = {
            "format": "best[height<=720]",
            "outtmpl": os.path.join(download_path, "%(title)s.%(ext)s"),
            "ignoreerrors": True,  # Skip errors and continue downloading other videos
        }
        with YoutubeDL(ydl_opts) as ydl:
            log_message(f"Processing playlist: {playlist_url}", log_file)
            result = ydl.extract_info(playlist_url, download=True)
            for entry in result["entries"]:
                if entry is None:  # Skip unavailable videos
                    log_message("Skipping unavailable video.", log_file)
                    continue
                video_title = entry["title"]
                video_url = entry["webpage_url"]

                if is_video_downloaded(video_title, download_path):
                    log_message(f"Skipping already downloaded video: {video_title}", log_file)
                else:
                    log_message(f"Downloading video: {video_title}", log_file)
                    ydl.download([video_url])
                    log_message(f"Downloaded video: {video_title}", log_file)

            log_message("Playlist processing completed.", log_file)
    except Exception as e:
        log_message(f"Failed to process playlist: {playlist_url}\nError: {e}", log_file)

def main():
    # Replace with your video or playlist URL and desired download folder
    url = input("Enter the YouTube video or playlist URL: ").strip()
    download_path = "./downloads"

    # Generate a unique log file name with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"logs/log_{timestamp}.txt"

    log_message("Script started.", log_file)

    # Check if the URL is for a single video or a playlist
    is_playlist = "list=" in url

    if is_playlist:
        log_message("Detected a playlist URL.", log_file)
        download_thread = threading.Thread(
            target=download_playlist,
            args=(url, download_path, log_file),
            daemon=True
        )
    else:
        log_message("Detected a single video URL.", log_file)
        download_thread = threading.Thread(
            target=download_video,
            args=(url, download_path, log_file),
            daemon=True
        )

    # Start the download process in a separate thread
    download_thread.start()
    log_message("Download process started in a separate thread.", log_file)
    download_thread.join()
    log_message("Script finished.", log_file)

if __name__ == "__main__":
    main()
