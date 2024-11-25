# yt-downloader-script

Youtube Downloader Python Script

# YouTube Playlist and Video Downloader

This Python script allows you to download all videos from a YouTube playlist or a single video at the highest available quality up to 720p. It is designed to handle large playlists, skip already downloaded videos, and maintain logs for each session.

---

## Features

- **Download Playlists or Single Videos**: Supports both YouTube playlists and individual video URLs.
- **Skip Duplicate Downloads**: Checks if a video has already been downloaded before attempting to download it again.
- **Threaded Processing**: Runs the download process in a separate thread to avoid blocking the main program.
- **Logs**: Generates a timestamped log file for each session, detailing the progress and errors encountered.

---

## Requirements

This script requires the following Python packages:

- `yt-dlp`
- `threading`
- `datetime`
- `os`

Install dependencies using pip:

```bash
pip install yt-dlp
```

---

## Installation and Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/kevinomyonga/yt-downloader-script
   ```
2. Navigate to the project directory:
   ```bash
   cd yt-downloader-script
   ```
3. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

Run the script as follows:

```bash
python yt_downloader.py
```

When prompted:

- Enter a YouTube playlist URL to download all videos in the playlist.
- Enter a single YouTube video URL to download only that video.

### Output

- Videos will be downloaded to the `downloads` directory.
- A log file for the session will be saved in the `logs` directory with a timestamped name, e.g., `logs/log_20241125_143200.txt`.

---

## License

This project is licensed under the terms of the [LICENSE](./LICENSE) file in this repository. Please review the license for usage guidelines.

---

## Maintainer

[![GitHub Kevin Omyonga](https://github.com/kevinomyonga.png?size=100)](https://github.com/kevinomyonga)  
**Kevin Omyonga**  
[Website](https://kevinomyonga.com) | [Twitter](https://twitter.com/kevinomyonga)

---

## Contribution

Contributions are welcome! If you encounter any issues or have ideas for improvements, feel free to open an issue or submit a pull request.

---

## Acknowledgements

This project uses the [yt-dlp](https://github.com/yt-dlp/yt-dlp) library for downloading videos from YouTube.

---

If you like this project, consider supporting its development:

[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-%23FFDD00?style=flat&logo=buy-me-a-coffee&logoColor=black)](https://www.buymeacoffee.com/KevinOmyonga)
