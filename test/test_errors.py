# coding: utf-8

import pytest
import gsm0338


@pytest.fixture
def codec():
    return gsm0338.Codec()


def test_decode_strict_basic(codec):
    with pytest.raises(ValueError) as exec_info:
        codec.decode(b'ab\x8Ad', errors='strict')
    assert "'gsm03.38' codec can't decode byte 0x8a in position 2" \
        == str(exec_info.value)


def test_decode_strict_extension(codec):
    with pytest.raises(ValueError) as exec_info:
        codec.decode(b'ab\x1b\x8ad', errors='strict')
    assert "'gsm03.38' codec can't decode byte 0x8a in position 3" \
        == str(exec_info.value)


def test_encode_strict(codec):
    with pytest.raises(ValueError) as exec_info:
        codec.encode(u'ab°c', errors='strict')
    assert "'gsm03.38' codec can't encode character %r in position 2" % u'°' \
        == str(exec_info.value)


def test_decode_replace(codec):
    assert codec.decode(b'ab\x8ad\x1b\x8ae', errors='replace') \
        == (u"ab\ufffdd\ufffde", 7)


def test_encode_replace(codec):
    assert codec.encode(u'ab°c', errors='replace') == (b'ab\x3fc', 4)


def test_decode_ignore(codec):
    assert codec.decode(b'ab\x8ad\x1b\x8ae', errors='ignore') \
        == (u"abde", 7)


def test_encode_ignore(codec):
    assert codec.encode(u'ab°c', errors='ignore') == (b'abc', 4)
