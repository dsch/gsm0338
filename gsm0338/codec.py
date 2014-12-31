import codecs
from six import unichr, byte2int, int2byte
from .unicode import *

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
    0x00: COMMERCIAL_AT,
    0x01: POUND_SIGN,
    0x02: DOLLAR_SIGN,
    0x03: YEN_SIGN,
    0x04: LATIN_SMALL_LETTER_E_WITH_GRAVE,
    0x05: LATIN_SMALL_LETTER_E_WITH_ACUTE,
    0x06: LATIN_SMALL_LETTER_U_WITH_GRAVE,
    0x07: LATIN_SMALL_LETTER_I_WITH_GRAVE,
    0x08: LATIN_SMALL_LETTER_O_WITH_GRAVE,
    0x09: LATIN_CAPITAL_LETTER_C_WITH_CEDILLA,
    0x0A: LINE_FEED,
    0x0B: LATIN_CAPITAL_LETTER_O_WITH_STROKE,
    0x0C: LATIN_SMALL_LETTER_O_WITH_STROKE,
    0x0D: CARRIAGE_RETURN,
    0x0E: LATIN_CAPITAL_LETTER_A_WITH_RING_ABOVE,
    0x0F: LATIN_SMALL_LETTER_A_WITH_RING_ABOVE,
    0x10: GREEK_CAPITAL_LETTER_DELTA,
    0x11: LOW_LINE,
    0x12: GREEK_CAPITAL_LETTER_PHI,
    0x13: GREEK_CAPITAL_LETTER_GAMMA,
    0x14: GREEK_CAPITAL_LETTER_LAMDA,
    0x15: GREEK_CAPITAL_LETTER_OMEGA,
    0x16: GREEK_CAPITAL_LETTER_PI,
    0x17: GREEK_CAPITAL_LETTER_PSI,
    0x18: GREEK_CAPITAL_LETTER_SIGMA,
    0x19: GREEK_CAPITAL_LETTER_THETA,
    0x1A: GREEK_CAPITAL_LETTER_XI,
    0x1B: ESCAPE,
    0x1C: LATIN_CAPITAL_LETTER_AE,
    0x1D: LATIN_SMALL_LETTER_AE,
    0x1E: LATIN_SMALL_LETTER_SHARP_S,
    0x1F: LATIN_CAPITAL_LETTER_E_WITH_ACUTE,
    0x24: CURRENCY_SIGN,
    0x40: INVERTED_EXCLAMATION_MARK,
    0x5B: LATIN_CAPITAL_LETTER_A_WITH_DIAERESIS,
    0x5C: LATIN_CAPITAL_LETTER_O_WITH_DIAERESIS,
    0x5D: LATIN_CAPITAL_LETTER_N_WITH_TILDE,
    0x5E: LATIN_CAPITAL_LETTER_U_WITH_DIAERESIS,
    0x5F: SECTION_SIGN,
    0x60: INVERTED_QUESTION_MARK,
    0x7B: LATIN_SMALL_LETTER_A_WITH_DIAERESIS,
    0x7C: LATIN_SMALL_LETTER_O_WITH_DIAERESIS,
    0x7D: LATIN_SMALL_LETTER_N_WITH_TILDE,
    0x7E: LATIN_SMALL_LETTER_U_WITH_DIAERESIS,
    0x7F: LATIN_SMALL_LETTER_A_WITH_GRAVE,
    0x1B0A: FORM_FEED,
    0x1B14:	CIRCUMFLEX_ACCENT,
    0x1B28:	LEFT_CURLY_BRACKET,
    0x1B29:	RIGHT_CURLY_BRACKET,
    0x1B2F:	REVERSE_SOLIDUS,
    0x1B3C:	LEFT_SQUARE_BRACKET,
    0x1B3D:	TILDE,
    0x1B3E:	RIGHT_SQUARE_BRACKET,
    0x1B40:	VERTICAL_LINE,
    0x1B65:	EURO_SIGN,
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
