# coding: utf-8

import pytest
import gsm0338
from six import int2byte


@pytest.fixture
def codec():
    return gsm0338.Codec()


GSM_BASIC_CHARACTER_SET = b"".join([int2byte(x) for x in range(27)]) +\
                          b"".join([int2byte(x) for x in range(28, 128)]) +\
                          b"\x1B\x0A\x1B\x14\x1B\x28\x1B\x29\x1B\x2F" \
                          b"\x1B\x3C\x1B\x3D\x1B\x3E\x1B\x40\x1B\x65"
UNICODE_BASIC_CHARACTER_SET = u"@£$¥èéùìòÇ\nØø\rÅåΔ_ΦΓΛΩΠΨΣΘΞÆæßÉ" \
                              u" !\"#¤%&'()*+,-./0123456789:;<=>?¡" \
                              u"ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÑÜ§¿" \
                              u"abcdefghijklmnopqrstuvwxyzäöñüà" \
                              u"\u000C^{}\\[~]|€"


def test_decode_alpha(codec):
    assert codec.decode(b'Abc') == (u'Abc', 3)


def test_decode_at(codec):
    assert codec.decode(b'\x00') == (u'@', 1)


def test_decode_extended(codec):
    assert codec.decode(b'\x1b\x28') == (u'{', 2)


def test_decode_basic_character_set(codec):
    assert codec.decode(GSM_BASIC_CHARACTER_SET) == \
        (UNICODE_BASIC_CHARACTER_SET, len(GSM_BASIC_CHARACTER_SET))


def test_encode_alpha(codec):
    assert codec.encode(u'Abc') == (b'Abc', 3)


def test_encode_at(codec):
    assert codec.encode(u'@') == (b'\x00', 1)


def test_encode_extended(codec):
    assert codec.encode(u'{') == (b'\x1b\x28', 1)


def test_encode_basic_character_set(codec):
    assert codec.encode(UNICODE_BASIC_CHARACTER_SET) == \
        (GSM_BASIC_CHARACTER_SET, len(UNICODE_BASIC_CHARACTER_SET))


def test_encode_spanish_single_shift():
    unicode_spanish_single_shift = u'ç\u000C^{}\[~]|ÁÍÓÚá€íóú'
    gsm_spanish_single_shift = b'\x1B\x09\x1B\x0A\x1B\x14\x1B\x28\x1B\x29' \
                               b'\x1B\x2F\x1B\x3C\x1B\x3D\x1B\x3E\x1B\x40' \
                               b'\x1B\x41\x1B\x49\x1B\x4F\x1B\x55\x1B\x61' \
                               b'\x1B\x65\x1B\x69\x1B\x6F\x1B\x75'

    codec = gsm0338.Codec(single_shift_decode_map=gsm0338.SINGLE_SHIFT_CHARACTER_SET_SPANISH)
    assert codec.encode(unicode_spanish_single_shift) == \
        (gsm_spanish_single_shift, len(unicode_spanish_single_shift))
