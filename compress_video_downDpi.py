import subprocess
import sys
import re
from tqdm import tqdm

def get_video_resolution(input_file):
    """
    Uses ffprobe to get the resolution (width and height) of the input video.
    It returns width and height on separate lines, then parses them.
    
    Returns:
        tuple: (width, height) as integers.
    """
    cmd = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        input_file
    ]
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        # Expecting two lines: first line is width, second line is height.
        lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        if len(lines) >= 2:
            width = int(lines[0])
            height = int(lines[1])
            return width, height
        else:
            raise Exception("Could not parse resolution. Output:\n" + result.stdout)
    except Exception as e:
        print("Error getting video resolution:", e)
        sys.exit(1)

def get_video_duration(input_file):
    """
    Uses ffprobe to get the duration of the input video in seconds.
    
    Returns:
        float: Duration in seconds.
    """
    cmd = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        input_file
    ]
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        duration = float(result.stdout.strip())
        return duration
    except Exception as e:
        print("Error getting video duration:", e)
        return None

def time_str_to_seconds(time_str):
    """
    Converts a time string formatted as HH:MM:SS.mmm to seconds.
    
    Args:
        time_str (str): Time string.
        
    Returns:
        float: Time in seconds.
    """
    try:
        parts = time_str.split(':')
        if len(parts) == 3:
            hours = int(parts[0])
            minutes = int(parts[1])
            seconds = float(parts[2])
            return hours * 3600 + minutes * 60 + seconds
        else:
            return float(time_str)
    except Exception:
        return 0.0

def compress_video(input_file, output_file, crf=28, preset='slow'):
    """
    Compress a video and downscale its resolution to 720p (if needed) without stretching.
    Also displays a progress bar during processing.
    
    Parameters:
        input_file (str): Path to the input video file.
        output_file (str): Path to the output (compressed) video file.
        crf (int): Constant Rate Factor, lower values mean better quality.
        preset (str): Encoding preset that controls speed vs. compression efficiency.
    """
    width, height = get_video_resolution(input_file)
    vf_filter = None
    if height > 720:
        # Downscale the video so that its height is 720 while preserving the aspect ratio.
        vf_filter = "scale=-2:720"
        print(f"Input height {height} exceeds 720. Downscaling video to 720p (width will be auto-calculated).")
    else:
        print(f"Input height {height} is within target. Keeping original resolution.")
    
    total_duration = get_video_duration(input_file)
    if total_duration is None:
        total_duration = 0
    
    # Build the ffmpeg command with progress output.
    command = [
        'ffmpeg',
        '-y',                   # Overwrite output file if it exists
        '-i', input_file,       # Input file
    ]
    
    if vf_filter:
        command.extend(['-vf', vf_filter])
    
    command.extend([
        '-vcodec', 'libx264',   # Use H.264 encoder
        '-crf', str(crf),       # Set quality level
        '-preset', preset,      # Set encoding preset
        '-acodec', 'copy',      # Copy audio without re-encoding
        '-progress', 'pipe:1',  # Print progress info to stdout
        output_file
    ])
    
    print("Starting compression...")
    
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    
    pbar = tqdm(total=total_duration, unit='s', desc='Processing', dynamic_ncols=True) if total_duration > 0 else None

    # Regular expression to capture out_time from ffmpeg progress output.
    out_time_re = re.compile(r'out_time=(\S+)')
    
    while True:
        line = process.stdout.readline()
        if not line:
            break
        line = line.strip()
        match = out_time_re.search(line)
        if match and pbar:
            current_time = time_str_to_seconds(match.group(1))
            if current_time > pbar.n:
                pbar.update(current_time - pbar.n)
    
    process.wait()
    if pbar:
        pbar.close()
    
    if process.returncode != 0:
        print("An error occurred during video compression.")
        sys.exit(1)
    else:
        print(f"Compression successful. Output saved as {output_file}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python compress_video.py input_file output_file")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    compress_video(input_path, output_path, crf=28, preset='slow')
