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


def run_fake_server() -> None:
    setup_logs()

    preview_payload = base64.b64encode(build_plaintext(1))
    logger.info(f"payload test : {preview_payload.decode('utf-8', errors='ignore')}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((HOST, PORT))
        server_sock.listen(1)
        logger.success(f"fake  server ready on {HOST}:{PORT}")


if __name__ == "__main__":
    run_fake_server()
