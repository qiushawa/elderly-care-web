import subprocess


def server(stream_id, port):
    """使用 FFmpeg 串流"""
    # ffmpeg -i https://stream.qiushawa.me/hls/qiushawa.m3u8 -f mjpeg -q:v 3 -r 25 tcp://127.0.0.1:8081 
    command = [
        "ffmpeg",
        "-i",
        f"http://eldercare.qiushawa.me/hls/{stream_id}.m3u8",
        "-f",
        "mjpeg",
        "-q:v",
        "3",
        "-r",
        "25",
        f"tcp://127.0.0.1:{port}"
    ]
    
    # ffmpeg -i http://eldercare.qiushawa.me/hls/123456.m3u8 -an -c:v mjpeg -q:v 10 -r 15 -f mjpeg tcp://127.0.0.1:8011
    print(f"FFmpeg command for {stream_id}: {' '.join(command)}")
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg error for {stream_id}: {e}")