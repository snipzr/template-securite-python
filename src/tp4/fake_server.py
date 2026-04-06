import base64
import socket
import sys

from loguru import logger

HOST = "127.0.0.1"
PORT = 8080
LOOP_COUNT = 87
RECV_TIMEOUT = 0.35


def setup_logs() -> None:
    logger.remove()
    logger.add(
        sys.stdout,
        format="<green>{time:HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>",
    )


def build_plaintext(loop_count: int) -> bytes:
    return f"mock-artifact-{loop_count:03d}".encode("utf-8")


def read_reply(accepted_conn: socket.socket) -> bytes:
    received_stream = b""
    while not received_stream.endswith(b"\n"):
        stream_chunk = accepted_conn.recv(4096)
        if not stream_chunk:
            raise ConnectionError("connection closed before newline")
        received_stream += stream_chunk
    return received_stream.strip()


def run_fake_server() -> None:
    setup_logs()

    preview_payload = base64.b64encode(build_plaintext(1))
    logger.info(f"payload test : {preview_payload.decode('utf-8', errors='ignore')}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((HOST, PORT))
        server_sock.listen(1)
        logger.success(f"fake  server ready on {HOST}:{PORT}")

        accepted_conn, peer = server_sock.accept()
        with accepted_conn:
            accepted_conn.settimeout(RECV_TIMEOUT)
            logger.info(f"client connected: {peer[0]}:{peer[1]}")

            for loop_count in range(1, LOOP_COUNT + 1):
                expected_text = build_plaintext(loop_count)
                encoded_chunk = base64.b64encode(expected_text)

                accepted_conn.sendall(b": " + encoded_chunk + b"\n")

                try:
                    decoded_reply = read_reply(accepted_conn)
                except socket.timeout:
                    logger.error(f"timeout at loop #{loop_count}")
                    return

                if decoded_reply != expected_text:
                    logger.error(
                        f"bad reply loop #{loop_count} | expected={expected_text!r} got={decoded_reply!r}"
                    )
                    accepted_conn.sendall(b"validation_failed\n")
                    return

                logger.success(f"loop #{loop_count} ok")

            accepted_conn.sendall(b"FLAG{mock_tp4_success}\n")
            logger.success("done, mock flag sent")


if __name__ == "__main__":
    run_fake_server()
