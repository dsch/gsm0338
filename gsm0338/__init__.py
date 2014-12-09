
__all__ = ["Codec"]

import codecs
from .codec import Codec, get_codec_info


def find_gsm0338(encoding):
    """
    Return codec info for 'gsm0338'
    :param encoding: name of the searched encoding
    """
    if encoding == Codec.NAME:
        return get_codec_info()
    return None


codecs.register(find_gsm0338)
