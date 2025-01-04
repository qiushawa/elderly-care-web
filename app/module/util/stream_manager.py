import threading
import subprocess

# 全域變數
streams = {}
stream_locks = {}
stream_threads = {}
BASE_TCP_PORT = 8011  # 基礎埠號
class StreamState:
    """管理全域變數的狀態"""

    def __init__(self):
        self.streams = {}  # 用於存儲串流數據
        self.stream_locks = {}  # 用於管理串流的線程鎖
        self.stream_threads = {}  # TCP 串流線程
        self.ffmpeg_threads = {}  # FFmpeg 線程

    def add_stream(self, stream_id):
        """初始化一個新的串流"""
        if stream_id in self.streams:
            raise ValueError(f"Stream {stream_id} already exists.")
        self.streams[stream_id] = b""
        self.stream_locks[stream_id] = threading.Lock()

    def remove_stream(self, stream_id):
        """刪除指定的串流"""
        if stream_id not in self.streams:
            raise ValueError(f"Stream {stream_id} does not exist.")
        del self.streams[stream_id]
        del self.stream_locks[stream_id]
        self.stream_threads.pop(stream_id, None)
        self.ffmpeg_threads.pop(stream_id, None)

    def set_tcp_thread(self, stream_id, thread):
        """設置 TCP 線程"""
        self.stream_threads[stream_id] = thread

    def set_ffmpeg_thread(self, stream_id, thread):
        """設置 FFmpeg 線程"""
        self.ffmpeg_threads[stream_id] = thread

class StreamManager:
    """動態管理串流來源"""

    def __init__(self, state:StreamState):
        self.state = state
        self.next_port = 8011

    def add_stream(self, stream_id, tcp_server_function, ffmpeg_server_function):
        """新增一個串流"""
        try:
            self.state.add_stream(stream_id)
        except ValueError as e:
            return str(e), 400
        
        port = self.next_port
        self.next_port += 1

        # 啟動 TCP 伺服器執行緒
        tcp_thread = threading.Thread(target=tcp_server_function, args=(stream_id, port, self.state), daemon=True)
        tcp_thread.start()
        self.state.set_tcp_thread(stream_id, tcp_thread)

        # 啟動 FFmpeg 執行緒
        ffmpeg_thread = threading.Thread(target=ffmpeg_server_function, args=(stream_id, port), daemon=True)
        ffmpeg_thread.start()
        self.state.set_ffmpeg_thread(stream_id, ffmpeg_thread)

        return f"Stream {stream_id} added on port {port}.", 200

    def remove_stream(self, stream_id):
        """移除一個串流"""
        try:
            self.state.remove_stream(stream_id)
        except ValueError as e:
            return str(e), 404

        return f"Stream {stream_id} removed.", 200
    # 檢查埠號是否被佔用 lsof -i
    def _check_port(self, port) -> bool:
        """檢查埠號是否被佔用"""
        return False
        # # if true, port is in use
        # result = subprocess.run(["lsof", "-i", f"{port}"], stdout=subprocess.PIPE)
        # return bool(result.stdout)
