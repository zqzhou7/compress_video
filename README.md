# Video Compressor

A Python-based tool that compresses video files using FFmpeg and ffprobe. The script automatically downscales videos to 720p (if necessary), applies H.264 compression with configurable quality parameters, and displays a real-time progress bar using tqdm.

## Features

- **Automatic Resolution Adjustment:**  
  If the input video’s resolution exceeds 720p in height, the tool resizes it to 720p while preserving the aspect ratio.
  
- **Configurable Compression Settings:**  
  Change the Constant Rate Factor (CRF) and encoding preset to balance between quality and compression speed.
  
- **Real-Time Progress Tracking:**  
  Uses the `tqdm` library to show live progress information during video compression.
  
- **Simple Command-Line Interface:**  
  Easily run the script from the command line by specifying the input and output file paths.

## Prerequisites

- **Python 3.x**  
- **FFmpeg & ffprobe:**  
  Ensure both FFmpeg and ffprobe are installed and available in your system's PATH.

- **Python Dependencies:**  
  Install the required Python package by running:  
  ```bash
  pip install tqdm

## Usage

Run the script from the command line with the input video file and output file path as arguments:
```bash
python compress_video.py input_video.mp4 output_video.mp4
```

## How It Works
- **Extract Video Information:**
  The script uses ffprobe to get the video's resolution and duration.

- **Adjust Resolution:**
If the height of the video exceeds 720p, it downscales the video while maintaining the aspect ratio using the scaling filter (scale=-2:720).

- **Run FFmpeg for Compression:**
It executes the ffmpeg command with the specified encoding options (H.264 codec, CRF, and preset). Audio is simply copied to preserve the original quality.

- **Display Progress:**
The script parses the FFmpeg progress output to update a progress bar displayed by tqdm.

## Code Overview
- **get_video_resolution(input_file):**
  Retrieves the width and height of the video using ffprobe.

- **get_video_duration(input_file):**
  Obtains the total duration of the video in seconds.

- **time_str_to_seconds(time_str):**
  Converts a timestamp string (HH:MM:SS.mmm) to seconds.

- **compress_video(input_file, output_file, crf, preset):**
  Main function that assembles the ffmpeg command, applies resolution adjustments if needed, tracks progress, and handles compression.

## Troubleshooting
- **FFmpeg/ffprobe not found:**
  Make sure these tools are installed and available in your PATH.

- **Permission Issues:**
  Use appropriate permissions, especially when overwriting files or installing system-wide tools.
