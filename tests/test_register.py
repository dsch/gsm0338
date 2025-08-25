# coding: utf-8

import gsm0338  # noqa: F401


def test_register_encoder():
    assert "{}".encode("gsm03.38") == b"\x1b(\x1b)"


def test_register_decoder():
    assert b"\x1b(\x1b)".decode("gsm03.38") == "{}"
