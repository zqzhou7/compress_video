import subprocess
import argparse
import re
from tqdm import tqdm

def get_video_duration(input_file):
    # Uses ffprobe to extract duration in seconds.
    result = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            input_file
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    try:
        return float(result.stdout.strip())
    except ValueError:
        raise RuntimeError("Could not determine video duration. Check the input file.")

def parse_timecode(time_str):
    """Converts HH:MM:SS.xxx into seconds."""
    try:
        h, m, s = time_str.strip().split(':')
        return int(h) * 3600 + int(m) * 60 + float(s)
    except Exception:
        return 0.0

def reduce_video(input_file, output_file, target_bitrate, preset):
    total_duration = get_video_duration(input_file)
    print(f"Video duration: {total_duration:.2f} sec")
    
    command = [
        "ffmpeg",
        "-y",
        "-i", input_file,
        "-b:v", target_bitrate,
        "-preset", preset,
        "-progress", "pipe:1",
        output_file
    ]
    
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    pbar = tqdm(total=total_duration, unit="sec", desc="Encoding progress")
    
    last_reported = 0.0
    while True:
        line = process.stdout.readline()
        if not line:
            break
        
        if "out_time=" in line:
            try:
                time_str = line.strip().split("out_time=")[-1]
                current_time = parse_timecode(time_str)
                if current_time > last_reported:
                    pbar.update(current_time - last_reported)
                    last_reported = current_time
            except Exception:
                pass
        
        if "progress=end" in line:
            pbar.n = total_duration
            pbar.refresh()
            break

    process.wait()
    pbar.close()
    print("Encoding finished.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reduce video file size by re-encoding with lower bitrate")
    parser.add_argument("input", help="Path to input video file")
    parser.add_argument("output", help="Path to output video file")
    parser.add_argument("--bitrate", default="10000k", help="Target video bitrate (default: 10000k)")
    parser.add_argument("--preset", default="fast", help="FFmpeg encoding preset (default: fast)")
    args = parser.parse_args()

    reduce_video(args.input, args.output, args.bitrate, args.preset)
