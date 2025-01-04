import subprocess


def server(stream_id, port):
    """使用 FFmpeg 串流"""
    # ffmpeg -i https://stream.qiushawa.me/hls/... -an -c:v mjpeg -q:v 10 -r 15 -f mjpeg tcp://127.0.0.1:8011

    command = [
        "ffmpeg",
        "-i", f"http://127.0.0.1:80/hls/{stream_id}.m3u8",
        "-an",
        "-c:v", "mjpeg",
        "-q:v", "10",
        "-r", "15",
        "-f", "mjpeg",
        f"tcp://127.0.0.1:{port}"
    ]
    print(f"FFmpeg command for {stream_id}: {' '.join(command)}")
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg error for {stream_id}: {e}")