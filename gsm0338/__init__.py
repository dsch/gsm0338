__all__ = ["Codec"]

import codecs
from .codec import Codec, get_codec_info, find_gsm0338
from .charset import SINGLE_SHIFT_CHARACTER_SET_SPANISH

codecs.register(find_gsm0338)
