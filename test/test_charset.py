# coding=utf-8

import gsm0338


def test_encode_spanish_single_shift():
    unicode_spanish_single_shift = u'ç\u000A^{}\[~]|ÁÍÓÚá€íóú'
    gsm_spanish_single_shift = b'\x1B\x09\x0A\x1B\x14\x1B\x28\x1B\x29' \
                               b'\x1B\x2F\x1B\x3C\x1B\x3D\x1B\x3E\x1B\x40' \
                               b'\x1B\x41\x1B\x49\x1B\x4F\x1B\x55\x1B\x61' \
                               b'\x1B\x65\x1B\x69\x1B\x6F\x1B\x75'

    codec = gsm0338.Codec(
        single_shift_decode_map=gsm0338.SINGLE_SHIFT_CHARACTER_SET_SPANISH
    )
    assert codec.encode(unicode_spanish_single_shift) == \
        (gsm_spanish_single_shift, len(unicode_spanish_single_shift))
