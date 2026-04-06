import base64
import binascii
import sys

from loguru import logger
from pwn import context

TARGET_HOST = "127.0.0.1"
TARGET_PORT = 8080
LOOP_COUNT = 82
DELIMITER = b": "
SOCKET_TIMEOUT = 0.45


def setup_logs() -> None:
    logger.remove()
    logger.add(
        sys.stdout,
        format="<green>{time:HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>",
    )


def decode_chunk(raw_b64_chunk: bytes) -> bytes:
    try:
        decoded_text = base64.b64decode(raw_b64_chunk, validate=True)
        return decoded_text

    except binascii.Error:
        b64_padding_fix = b"=" * (-len(raw_b64_chunk) % 4)
        decoded_text = base64.b64decode(raw_b64_chunk + b64_padding_fix, validate=False)
        return decoded_text


def run_decoder() -> None:
    setup_logs()
    context.log_level = "error"
    logger.info("tp4 client pret : base logs + decodeur base64")

    test_chunk = b"bW9jay10cDQtY2xpZW50"
    decoded_test = decode_chunk(test_chunk)
    logger.success(decoded_test.decode("utf-8", errors="ignore"))


if __name__ == "__main__":
    run_decoder()