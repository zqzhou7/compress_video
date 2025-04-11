# Video Compressor

A Python-based tool that compresses video files using FFmpeg and ffprobe. This repository includes two scripts that use similar mechanisms (real-time progress via tqdm, FFmpeg re-encoding) but differ in how they handle resolution:

- **Downscale Resolution & Compress:**  
  The `compress_video_downDpi.py` script automatically downscales videos to 720p (if necessary) and applies H.264 compression with configurable quality parameters.

- **Compress Without Changing Resolution:**  
  The `compress_video_downDps.py` script compresses the video to reduce the file size without altering the original resolution or frame rate.

## Features

- **Automatic Resolution Adjustment:**  
  - For videos where the input’s resolution exceeds 720p in height, the `compress_video_downDpi.py` script resizes the video to 720p while preserving the aspect ratio.
  
- **Compression Options without Resolution Change:**  
  - The `compress_video_downDps.py` script compresses the video by reducing the bitrate only, keeping the original video resolution and frame rate intact.
  
- **Configurable Compression Settings:**  
  Both tools allow you to modify encoding settings. You can adjust the Constant Rate Factor (CRF) and preset for the downscaling method, or the bitrate and preset for the compression-only method, to balance quality, file size, and speed.
  
- **Real-Time Progress Tracking:**  
  Uses the `tqdm` library to show live progress information during video compression.
  
- **Simple Command-Line Interface:**  
  Easily run either script from the command line by specifying the input and output file paths and any additional encoding parameters.

## Prerequisites

- **Python 3.x**

- **FFmpeg & ffprobe:**  
  Ensure both FFmpeg and ffprobe are installed and available in your system’s PATH.

- **Python Dependencies:**  
  Install the required Python package by running:
  ```bash
  pip install tqdm

## Usage

### 1. Downscale Resolution & Compress

This script reduces the file size and also downsizes the resolution to 720p if the video’s height exceeds that threshold.

Run the script with:
```bash
python compress_video_downDpi.py input_video.mp4 output_video.mp4 [--crf <value>] [--preset <value>]
```

Example:

```
python compress_video_downDpi.py input_video.mp4 output_video.mp4 --crf 23 --preset fast
```

### 2. Compress Without Changing Resolution
This script reduces the file size by adjusting the video bitrate while preserving the original resolution and frame rate.

Run the script with:

```
python compress_video_downDps.py input_video.mp4 output_video.mp4 [--bitrate <value>] [--preset <value>]
```

Example:

```
python compress_video_downDps.py input_video.mp4 output_video.mp4 --bitrate 10000k --preset fast
```

## How It Works
- **Extract Video Information:**
  Both scripts use `ffprobe` to obtain key metadata such as the video’s resolution (for the downscaling version) and duration. This information is vital for updating the progress bar.

- **Adjust Resolution:**
If the height of the video exceeds 720p, it downscales the video while maintaining the aspect ratio using the scaling filter (scale=-2:720).

- **Run FFmpeg for Compression:**
Both scripts execute an FFmpeg command with the chosen parameters:
  - **For downscaling:** Applies resolution adjustments, H.264 codec compression with CRF and preset options, and copies audio to maintain original quality.
  - **For compression-only:** Adjusts the video bitrate (using `-b:v`) and applies the preset without any scaling filters.

- **Display Progress:**
Both scripts parse FFmpeg’s progress output to update a live progress bar displayed by `tqdm`, giving you a visual indication of the compression progress.

## Code Overview
- **get_video_resolution(input_file):**
Retrieves the width and height of the video using `ffprobe` (used in `compress_video_downDpi.py`).

- **get_video_duration(input_file):**
Obtains the total duration of the video in seconds (common to both scripts).

- **time_str_to_seconds(time_str):**
Converts a timestamp (in `HH:MM:SS.mmm` format) into seconds.

- **compress_video(...):**
Assembles and executes the FFmpeg command with appropriate options (resolution adjustment and CRF for downscaling, or bitrate for compression-only), handles progress tracking, and completes the compression process.

## Troubleshooting
- **FFmpeg/ffprobe Not Found:**
Ensure that these tools are installed and available in your PATH.

- **Permission Issues:**
Use appropriate permissions especially when overwriting files or installing system-wide tools.

- **Python Package Errors:**
Verify that you have installed all required dependencies (e.g., `tqdm`).

By using these two scripts, you have the flexibility to choose your preferred compression method—downscaling to 720p when needed, or simply reducing the file size while maintaining the original resolution and quality. 
