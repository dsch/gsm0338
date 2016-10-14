# coding: utf-8

import codecs
import gsm0338


def test_register_encoder():
    assert '{}'.encode('gsm03.38') == b'\x1b(\x1b)'


def test_register_decoder():
    assert b'\x1b(\x1b)'.decode('gsm03.38') == '{}'


def test_find_returns_codecinfo_type():
    assert isinstance(gsm0338.find_gsm0338('gsm03.38'), codecs.CodecInfo)


def test_find_returns_codecinfo_name():
    assert gsm0338.find_gsm0338('gsm03.38').name == 'gsm03.38'


def test_find_returns_codecinfo_caseinsensitve():
    assert gsm0338.find_gsm0338('GSM03.38').name == 'gsm03.38'
