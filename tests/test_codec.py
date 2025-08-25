# coding: utf-8

import pytest

import gsm0338


@pytest.fixture
def codec():
    return gsm0338.Codec()


GSM_BASIC_CHARACTER_SET = (
    bytes(range(27))
    + bytes(range(28, 128))
    + b"\x1b\x0a\x1b\x14\x1b\x28\x1b\x29\x1b\x2f"
    b"\x1b\x3c\x1b\x3d\x1b\x3e\x1b\x40\x1b\x65"
)
UNICODE_BASIC_CHARACTER_SET = (
    "@£$¥èéùìòÇ\nØø\rÅåΔ_ΦΓΛΩΠΨΣΘΞÆæßÉ"
    " !\"#¤%&'()*+,-./0123456789:;<=>?¡"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÑÜ§¿"
    "abcdefghijklmnopqrstuvwxyzäöñüà"
    "\u000c^{}\\[~]|€"
)


def test_decode_alpha(codec):
    assert codec.decode(b"Abc") == ("Abc", 3)


def test_decode_at(codec):
    assert codec.decode(b"\x00") == ("@", 1)


def test_decode_extended(codec):
    assert codec.decode(b"\x1b\x28") == ("{", 2)


def test_decode_basic_character_set(codec):
    assert codec.decode(GSM_BASIC_CHARACTER_SET) == (
        UNICODE_BASIC_CHARACTER_SET,
        len(GSM_BASIC_CHARACTER_SET),
    )


def test_encode_alpha(codec):
    assert codec.encode("Abc") == (b"Abc", 3)


def test_encode_at(codec):
    assert codec.encode("@") == (b"\x00", 1)


def test_encode_extended(codec):
    assert codec.encode("{") == (b"\x1b\x28", 1)


def test_encode_basic_character_set(codec):
    assert codec.encode(UNICODE_BASIC_CHARACTER_SET) == (
        GSM_BASIC_CHARACTER_SET,
        len(UNICODE_BASIC_CHARACTER_SET),
    )
