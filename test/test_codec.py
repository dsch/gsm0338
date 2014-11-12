# coding: utf-8

import pytest


@pytest.fixture
def codec():
    import gsm0338
    return gsm0338.Codec()


GSM_BASIC_CHARACTER_SET = "".join(map(chr, range(27) + range(28, 128)))
UNICODE_BASIC_CHARACTER_SET = u"@£$¥èéùìòÇ\nØø\rÅåΔ_ΦΓΛΩΠΨΣΘΞÆæßÉ" \
                              u" !\"#¤%&'()*+,-./0123456789:;<=>?¡" \
                              u"ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÑÜ§¿" \
                              u"abcdefghijklmnopqrstuvwxyzäöñüà"


class TestCodec:
    def test_decode_basic_character_set(self, codec):
        assert codec.decode(GSM_BASIC_CHARACTER_SET) == \
            (UNICODE_BASIC_CHARACTER_SET, len(GSM_BASIC_CHARACTER_SET))

    def test_encode_basic_character_set(self, codec):
        assert codec.encode(UNICODE_BASIC_CHARACTER_SET) == \
            (GSM_BASIC_CHARACTER_SET, len(GSM_BASIC_CHARACTER_SET))
