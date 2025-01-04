import socket, subprocess

def server(stream_id, port, streams, stream_locks):
    """接收 MJPEG 串流並存入對應緩衝區"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(('127.0.0.1', port))
        server_socket.listen(1)
        print(f"TCP Server for {stream_id} listening on port {port}...")

        conn, addr = server_socket.accept()
        print(f"Connection established for {stream_id} from {addr}")

        data_buffer = b""
        try:
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                data_buffer += data
                start_idx = data_buffer.find(b'\xff\xd8')
                end_idx = data_buffer.find(b'\xff\xd9')

                if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                    frame = data_buffer[start_idx:end_idx + 2]
                    with stream_locks[stream_id]:
                        streams[stream_id] = frame
                    data_buffer = data_buffer[end_idx + 2:]
        except Exception as e:
            print(f"Error in TCP server for {stream_id}: {e}")
        finally:
            conn.close()
            print(f"Connection for {stream_id} closed.")

