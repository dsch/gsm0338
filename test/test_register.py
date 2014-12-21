# coding: utf-8

import gsm0338


def find_gsm0338(encoding):
    """Return the codec for 'gsm0338'.
    """
    if encoding == 'gsm0338':
        return gsm0338.getregentry()
    return None


def test_register_encoder():
    assert '{}'.encode('gsm0338') == b'\x1b(\x1b)'


def test_register_decoder():
    assert b'\x1b(\x1b)'.decode('gsm0338') == '{}'
