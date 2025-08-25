# coding=utf-8

import gsm0338


def test_encode_spanish_single_shift():
    unicode_spanish_single_shift = "ç\u000a^{}\\[~]|ÁÍÓÚá€íóú"
    gsm_spanish_single_shift = (
        b"\x1b\x09\x0a\x1b\x14\x1b\x28\x1b\x29"
        b"\x1b\x2f\x1b\x3c\x1b\x3d\x1b\x3e\x1b\x40"
        b"\x1b\x41\x1b\x49\x1b\x4f\x1b\x55\x1b\x61"
        b"\x1b\x65\x1b\x69\x1b\x6f\x1b\x75"
    )

    codec = gsm0338.Codec(
        single_shift_decode_map=gsm0338.SINGLE_SHIFT_CHARACTER_SET_SPANISH
    )
    assert codec.encode(unicode_spanish_single_shift) == (
        gsm_spanish_single_shift,
        len(unicode_spanish_single_shift),
    )
