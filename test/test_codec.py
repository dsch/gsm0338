# coding: utf-8

import pytest
import gsm0338


@pytest.fixture
def codec():
    return gsm0338.Codec()


GSM_BASIC_CHARACTER_SET = "".join(map(chr, range(27) + range(28, 128))) +\
                          "\x1B\x0A\x1B\x14\x1B\x28\x1B\x29\x1B\x2F" \
                          "\x1B\x3C\x1B\x3D\x1B\x3E\x1B\x40\x1B\x65"
UNICODE_BASIC_CHARACTER_SET = u"@£$¥èéùìòÇ\nØø\rÅåΔ_ΦΓΛΩΠΨΣΘΞÆæßÉ" \
                              u" !\"#¤%&'()*+,-./0123456789:;<=>?¡" \
                              u"ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÑÜ§¿" \
                              u"abcdefghijklmnopqrstuvwxyzäöñüà" \
                              u"\u000C^{}\[~]|€"


def test_decode_basic_character_set(codec):
    assert codec.decode(GSM_BASIC_CHARACTER_SET) == \
           (UNICODE_BASIC_CHARACTER_SET, len(UNICODE_BASIC_CHARACTER_SET))


def test_encode_basic_character_set(codec):
    assert codec.encode(UNICODE_BASIC_CHARACTER_SET) == \
           (GSM_BASIC_CHARACTER_SET, len(GSM_BASIC_CHARACTER_SET))
