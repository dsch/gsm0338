# coding: utf-8

import pytest
import gsm0338


@pytest.fixture
def codec():
    return gsm0338.Codec()


def test_decode_strict_basic(codec):
    with pytest.raises(ValueError) as exec_info:
        codec.decode(b'ab\x8A', errors='strict')
    assert "'gsm0338' codec can't decode byte 0x8a in position 2" \
           == str(exec_info.value)


def test_decode_strict_extension(codec):
    with pytest.raises(ValueError) as exec_info:
        codec.decode(b'ab\x1b\x8a', errors='strict')
    assert "'gsm0338' codec can't decode byte 0x8a in position 3" \
           == str(exec_info.value)


def test_encode_strict(codec):
    with pytest.raises(ValueError) as exec_info:
        codec.encode(u'ab°', errors='strict')
    assert "'gsm0338' codec can't encode character %r in position 2" % u'°' \
           == str(exec_info.value)
