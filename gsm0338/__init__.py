import codecs
from .charset import SINGLE_SHIFT_CHARACTER_SET_SPANISH
from .codec import Codec, find_gsm0338, get_codec_info

__all__ = ['SINGLE_SHIFT_CHARACTER_SET_SPANISH', 'Codec', 'find_gsm0338', 'get_codec_info']

codecs.register(find_gsm0338)
