# coding: utf-8
"""
This example demonstrates how to use your own error handler to normalize characters based on unicode normalization
"""

import codecs
import unicodedata

import gsm0338  # noqa: F401


def normalize_errors(exception):
    """Use unicode normalization to replace unencodable characters by there normalized form
    :param exception: a UnicodeEncodeError instance, which contains information about the location of the error
    :return: tuple with a replacement for the unencodable part of the input and a position where encoding should
    continue
    """
    data = exception.object[exception.start : exception.end]
    normalized = unicodedata.normalize("NFKD", data)
    replacement = b"".join(
        [c.encode(exception.encoding, errors="ignore") for c in normalized]
    )
    return replacement, exception.end


# register your own error handler
codecs.register_error("normalize", normalize_errors)

assert "êëçîï→".encode("gsm03.38", errors="normalize") == b"eecii"
