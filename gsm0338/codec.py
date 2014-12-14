import codecs
from six import unichr, byte2int, int2byte

# Codec APIs


class Codec(codecs.Codec):
    """
    Stateless encoder and decoder for GSM 03.38
    """

    NAME = 'gsm0338'
    _ESCAPE = 0x1b

    def encode(self, input, errors='strict'):
        """
        Encode string to byte array
        :param input: string (unicode) object to convert to byte array
        :param errors: defines the error handling to apply
        :return: returns a tuple (output object, length consumed)
        """
        encode_buffer = b''
        consumed = 0
        for c in input:
            consumed += 1
            num = None
            try:
                num = _ENCODING_MAP[ord(c)]
            except KeyError as ex:
                if errors == 'replace':
                    num = 0x3f
                elif errors == 'ignore':
                    pass
                else:
                    raise ValueError("'%s' codec can't encode character %r in position %d" %
                                     (self.NAME, c, consumed - 1))
            if num is not None:
                if num & 0xff00:
                    encode_buffer += int2byte(self._ESCAPE)
                encode_buffer += int2byte(num & 0xff)
        return encode_buffer, consumed

    def decode(self, input, errors='strict'):
        """
        Decode byte array to string
        :param input: byte array to convert to unicode string
        :param errors: defines the error handling to apply
        :return: returns a tuple (output object, length consumed)
        """
        decode_buffer = u""
        consumed = 0

        num = 0
        for value in input:
            consumed += 1
            num |= byte2int([value])
            if num == self._ESCAPE:
                num <<= 8
                continue
            try:
                decode_buffer += unichr(_DECODING_MAP[num])
            except KeyError as ex:
                if errors == 'replace':
                    decode_buffer += u'\ufffd'
                elif errors == 'ignore':
                    pass
                else:
                    if num & (self._ESCAPE << 8):
                        raise ValueError("'%s' codec can't decode byte 0x%x in position %d" %
                                         (self.NAME, ex.args[0] & 0xff, consumed - 1))
                    else:
                        raise ValueError("'%s' codec can't decode byte 0x%x in position %d" %
                                         (self.NAME, ex.args[0], consumed - 1))
            num = 0
        return decode_buffer, consumed


class IncrementalEncoder(codecs.IncrementalEncoder):

    def encode(self, input, final=False):
        return codecs.charmap_encode(input, self.errors, _ENCODING_MAP)[0]


class IncrementalDecoder(codecs.IncrementalDecoder):

    def decode(self, input, final=False):
        return codecs.charmap_decode(input, self.errors, _DECODING_MAP)[0]


class StreamWriter(Codec, codecs.StreamWriter):
    """
    StreamWriter: for GSM 03.38 codec
    """
    pass


class StreamReader(Codec, codecs.StreamReader):
    """
    StreamReader: for GSM 03.38 codec
    """
    pass


# encodings module API
def get_codec_info():
    """
    encodings module API
    :return: CodecInfo for gsm0338 codec
    """
    return codecs.CodecInfo(
        name='gsm03.38',
        encode=Codec().encode,
        decode=Codec().decode,
        incrementalencoder=IncrementalEncoder,
        incrementaldecoder=IncrementalDecoder,
        streamwriter=StreamWriter,
        streamreader=StreamReader,
    )


_DECODING_MAP = codecs.make_identity_dict(range(127))
_DECODING_MAP.update({
    0x00: 0x0040,  # COMMERCIAL AT
    0x01: 0x00A3,  # POUND SIGN
    0x02: 0x0024,  # DOLLAR SIGN
    0x03: 0x00A5,  # YEN SIGN
    0x04: 0x00E8,  # LATIN SMALL LETTER E WITH GRAVE
    0x05: 0x00E9,  # LATIN SMALL LETTER E WITH ACUTE
    0x06: 0x00F9,  # LATIN SMALL LETTER U WITH GRAVE
    0x07: 0x00EC,  # LATIN SMALL LETTER I WITH GRAVE
    0x08: 0x00F2,  # LATIN SMALL LETTER O WITH GRAVE
    # 0x09: 0x00E7,  # LATIN SMALL LETTER C WITH CEDILLA
    0x09: 0x00C7,  # LATIN CAPITAL LETTER C WITH CEDILLA
    0x0B: 0x00D8,  # LATIN CAPITAL LETTER O WITH STROKE
    0x0C: 0x00F8,  # LATIN SMALL LETTER O WITH STROKE
    0x0E: 0x00C5,  # LATIN CAPITAL LETTER A WITH RING ABOVE
    0x0F: 0x00E5,  # LATIN SMALL LETTER A WITH RING ABOVE
    0x10: 0x0394,  # GREEK CAPITAL LETTER DELTA
    0x11: 0x005F,  # LOW LINE
    0x12: 0x03A6,  # GREEK CAPITAL LETTER PHI
    0x13: 0x0393,  # GREEK CAPITAL LETTER GAMMA
    0x14: 0x039B,  # GREEK CAPITAL LETTER LAMDA
    0x15: 0x03A9,  # GREEK CAPITAL LETTER OMEGA
    0x16: 0x03A0,  # GREEK CAPITAL LETTER PI
    0x17: 0x03A8,  # GREEK CAPITAL LETTER PSI
    0x18: 0x03A3,  # GREEK CAPITAL LETTER SIGMA
    0x19: 0x0398,  # GREEK CAPITAL LETTER THETA
    0x1A: 0x039E,  # GREEK CAPITAL LETTER XI
    # 0x1B: 0x00A0,  # ESCAPE TO EXTENSION TABLE (or displayed as NBSP)
    0x1C: 0x00C6,  # LATIN CAPITAL LETTER AE
    0x1D: 0x00E6,  # LATIN SMALL LETTER AE
    0x1E: 0x00DF,  # LATIN SMALL LETTER SHARP S (German)
    0x1F: 0x00C9,  # LATIN CAPITAL LETTER E WITH ACUTE
    0x24: 0x00A4,  # CURRENCY SIGN
    0x40: 0x00A1,  # INVERTED EXCLAMATION MARK
    0x5B: 0x00C4,  # LATIN CAPITAL LETTER A WITH DIAERESIS
    0x5C: 0x00D6,  # LATIN CAPITAL LETTER O WITH DIAERESIS
    0x5D: 0x00D1,  # LATIN CAPITAL LETTER N WITH TILDE
    0x5E: 0x00DC,  # LATIN CAPITAL LETTER U WITH DIAERESIS
    0x5F: 0x00A7,  # SECTION SIGN
    0x60: 0x00BF,  # INVERTED QUESTION MARK
    0x7B: 0x00E4,  # LATIN SMALL LETTER A WITH DIAERESIS
    0x7C: 0x00F6,  # LATIN SMALL LETTER O WITH DIAERESIS
    0x7D: 0x00F1,  # LATIN SMALL LETTER N WITH TILDE
    0x7E: 0x00FC,  # LATIN SMALL LETTER U WITH DIAERESIS
    0x7F: 0x00E0,  # LATIN SMALL LETTER A WITH GRAVE
    0x1B0A: 0x000C,  # FORM FEED
    0x1B14:	0x005E,  # CIRCUMFLEX ACCENT
    0x1B28:	0x007B,  # LEFT CURLY BRACKET
    0x1B29:	0x007D,  # RIGHT CURLY BRACKET
    0x1B2F:	0x005C,  # REVERSE SOLIDUS
    0x1B3C:	0x005B,  # LEFT SQUARE BRACKET
    0x1B3D:	0x007E,  # TILDE
    0x1B3E:	0x005D,  # RIGHT SQUARE BRACKET
    0x1B40:	0x007C,  # VERTICAL LINE
    0x1B65:	0x20AC,  # EURO SIGN
})


# 0x41: 0x0391  # GREEK CAPITAL LETTER ALPHA
# 0x42: 0x0392  # GREEK CAPITAL LETTER BETA
# 0x45: 0x0395  # GREEK CAPITAL LETTER EPSILON
# 0x48: 0x0397  # GREEK CAPITAL LETTER ETA
# 0x49: 0x0399  # GREEK CAPITAL LETTER IOTA
# 0x4B: 0x039A  # GREEK CAPITAL LETTER KAPPA
# 0x4D: 0x039C  # GREEK CAPITAL LETTER MU
# 0x4E: 0x039D  # GREEK CAPITAL LETTER NU
# 0x4F: 0x039F  # GREEK CAPITAL LETTER OMICRON
# 0x50: 0x03A1  # GREEK CAPITAL LETTER RHO
# 0x54: 0x03A4  # GREEK CAPITAL LETTER TAU
# 0x58: 0x03A7  # GREEK CAPITAL LETTER CHI
# 0x59: 0x03A5  # GREEK CAPITAL LETTER UPSILON
# 0x5A: 0x0396  # GREEK CAPITAL LETTER ZETA


_ENCODING_MAP = codecs.make_encoding_map(_DECODING_MAP)
