import pytest


@pytest.fixture
def codec():
    import gsm0338
    print gsm0338.codecs
    return gsm0338.Codec()


def test_decode(codec):
    assert codec.decode('\x00\x41\x42\x43') == (u'@ABC', 4)


def test_encode(codec):
    assert codec.encode(u'@ABC') == ('\x00\x41\x42\x43', 4)
