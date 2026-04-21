import pytest
from src.tp2.utils.config import hex_to_bytes

def test_hex_to_bytes_simple():
    assert hex_to_bytes("414243") == b"ABC"

def test_hex_to_bytes_with_formatting():
    assert hex_to_bytes("\\x41\\x42\\x43") == b"ABC"
    assert hex_to_bytes("41 42 43") == b"ABC"

def test_hex_to_bytes_empty():
    assert hex_to_bytes("") == b""

def test_hex_to_bytes_invalid_chars_ignored():
    assert hex_to_bytes("4Z1X4Y2W4U3") == b"ABC"
