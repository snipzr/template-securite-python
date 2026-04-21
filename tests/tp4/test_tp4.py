import pytest
import base64
from src.tp4.main import decode_chunk
from src.tp4.fake_server import build_plaintext

def test_decode_chunk_valid_base64():
    valid_b64 = base64.b64encode(b"Hello World")
    assert decode_chunk(valid_b64) == b"Hello World"

def test_decode_chunk_missing_padding():
    valid_b64 = base64.b64encode(b"Test padding").decode('utf-8')
    missing_padding = valid_b64.rstrip('=')
    
    assert decode_chunk(missing_padding.encode('utf-8')) == b"Test padding"

def test_build_plaintext_single_digit():
    assert build_plaintext(1) == b"mock-artifact-001"
    assert build_plaintext(5) == b"mock-artifact-005"

def test_build_plaintext_large_digit():
    assert build_plaintext(100) == b"mock-artifact-100"
    assert build_plaintext(999) == b"mock-artifact-999"
