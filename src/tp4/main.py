import base64
import binascii
import sys

from loguru import logger
from pwn import context, remote

TARGET_HOST = "127.0.0.1"
TARGET_PORT = 8080
LOOP_COUNT = 87
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


def read_b64_chunk(target_conn):
    target_conn.recvuntil(DELIMITER, timeout=SOCKET_TIMEOUT)
    raw_b64_chunk = target_conn.recvline(timeout=SOCKET_TIMEOUT).strip()

    if raw_b64_chunk:
        return raw_b64_chunk

    raw_b64_chunk = target_conn.recvregex(
        rb"[A-Za-z0-9+/]{4,}={0,2}\r?\n",
        timeout=SOCKET_TIMEOUT,
    ).strip()
    return raw_b64_chunk


def run_decoder() -> None:
    setup_logs()
    context.log_level = "error"
    logger.info("tp4 client pret : boucle decode + send")

    target_conn = None
    try:
        target_conn = remote(TARGET_HOST, TARGET_PORT, timeout=0.60)
        logger.success(f"connected to {TARGET_HOST}:{TARGET_PORT}")

        for loop_count in range(1, LOOP_COUNT + 1):
            raw_b64_chunk = read_b64_chunk(target_conn)
            decoded_text = decode_chunk(raw_b64_chunk)
            logger.info(f"loop #{loop_count} | raw len={len(raw_b64_chunk)}")
            target_conn.sendline(decoded_text)

        final_line = target_conn.recvline(timeout=0.60).strip()
        if final_line:
            logger.success(f"server reply: {final_line.decode('utf-8', errors='ignore')}")

    except EOFError:
        logger.warning("server closed , fin de challenge")
    except KeyboardInterrupt:
        logger.warning("stop manuel")
    except Exception as err:
        logger.error(f"decoder error: {err}")
    finally:
        if target_conn is not None:
            target_conn.close()
            logger.info("connection closed")


if __name__ == "__main__":
    run_decoder()