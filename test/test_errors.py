# coding: utf-8

import sys

import pytest

import gsm0338


@pytest.fixture
def codec():
    return gsm0338.Codec()


def test_decode_strict_basic(codec):
    with pytest.raises(ValueError) as exec_info:
        codec.decode(b'ab\x8Ad', errors='strict')
    assert "'gsm03.38' codec can't decode byte 0x8a in position 2: invalid sequence" \
           == str(exec_info.value)


def test_decode_strict_extension(codec):
    with pytest.raises(ValueError) as exec_info:
        codec.decode(b'ab\x1b\x8ad', errors='strict')
    assert "'gsm03.38' codec can't decode bytes in position 2-3: invalid sequence" \
           == str(exec_info.value)


def test_encode_strict(codec):
    with pytest.raises(ValueError) as exec_info:
        codec.encode(u'ab°c', errors='strict')
    assert "'gsm03.38' codec can't encode character %s'\\x%x' in position 2: character not mapped" % (
        'u' if sys.version_info[0] < 3 else '', 0xB0) == str(exec_info.value)


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
