import subprocess


def server(stream_id, port):
    """使用 FFmpeg 串流"""

    command = [
        "ffmpeg",
        "-i", f"https://stream.qiushawa.me/hls/{stream_id}.m3u8",
        "-an",
        "-c:v", "mjpeg",
        "-q:v", "10",
        "-r", "15",
        "-f", "mjpeg",
        f"tcp://127.0.0.1:{port}"
    ]
    
    # ffmpeg -i http://eldercare.qiushawa.me/hls/123456.m3u8 -an -c:v mjpeg -q:v 10 -r 15 -f mjpeg tcp://127.0.0.1:8011
    print(f"FFmpeg command for {stream_id}: {' '.join(command)}")
    try:
        subprocess.Popen(command)
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg error for {stream_id}: {e}")