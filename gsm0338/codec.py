import codecs
import sys
import unicodedata

from .charset import BASIC_CHARACTER_SET, BASIC_CHARACTER_SET_EXTENSION


# Codec APIs
class Codec(codecs.Codec):
    """
    Stateless encoder and decoder for GSM 03.38
    """

    NAME = 'gsm03.38'
    __ESCAPE = 0x1b

    def __init__(self, locking_shift_decode_map=BASIC_CHARACTER_SET,
                 single_shift_decode_map=BASIC_CHARACTER_SET_EXTENSION):
        if sys.version_info[0] < 3:
            self.__int2byte = chr
            self.__byte2int = ord
            self.__unicode_lookup = Codec.__unicode_lookup27
        else:
            self.__int2byte = lambda i: bytes((i,))
            self.__byte2int = lambda i: i
            self.__unicode_lookup = unicodedata.lookup

        self._decode_map = dict(
            [(key, self.__unicode_lookup(name)) for key, name in locking_shift_decode_map.items()])
        self._decode_map.update(
            dict(((self.__ESCAPE << 8 | key), self.__unicode_lookup(name))
                 for key, name in single_shift_decode_map.items()))

        self._encoding_map = codecs.make_encoding_map(self._decode_map)

    @staticmethod
    def __unicode_lookup27(name):
        """unicodedata lookup function only used for Python 2.7"""
        try:
            return unicodedata.lookup(name)
        except KeyError:
            unicode_lookup_fallback = {
                'LINE FEED': u'\x0A',
                'FORM FEED': u'\x0C',
                'CARRIAGE RETURN': u'\x0D',
                'ESCAPE': u'\x1B',
            }
            return unicode_lookup_fallback[name]

    def encode(self, input, errors='strict'):
        """
        Encode string to byte array
        :param str input: string (unicode) object to convert to byte array
        :param str errors: defines the error handling to apply
        :return: returns a tuple (output object, length consumed)
        :rtype: (bytes,int)
        """

        error_handler = None  # cache for error handler
        encode_buffer = b''
        pos = 0
        input_length = len(input)
        while pos < input_length:
            try:
                encode_buffer += self.__encode_character(input[pos])
                pos += 1
            except KeyError:
                if error_handler is None:
                    error_handler = codecs.lookup_error(errors)
                encode_error = UnicodeEncodeError(self.NAME, input, pos, pos + 1, 'character not mapped')
                replacement, pos = error_handler(encode_error)
                if replacement:
                    encode_buffer += self.__encode_character(replacement[0])
        return encode_buffer, pos

    def __encode_character(self, character):
        append_buffer = b''
        num = self._encoding_map[character]
        if num & 0xff00:
            append_buffer += self.__int2byte(self.__ESCAPE)
        append_buffer += self.__int2byte(num & 0xff)
        return append_buffer

    def decode(self, input, errors='strict'):
        """
        Decode byte array to string
        :param bytes input: byte array to convert to unicode string
        :param str errors: defines the error handling to apply
        :return: returns a tuple (output object, length consumed)
        :rtype: (str,int)
        """

        error_handler = None  # cache for error handler
        decode_buffer = u""

        start_pos = 0
        next_pos = 0
        num = 0
        input_length = len(input)
        while next_pos < input_length:
            try:
                num |= self.__byte2int(input[next_pos])
                next_pos += 1
                if num == self.__ESCAPE:
                    num <<= 8
                    continue
                decode_buffer += self._decode_map[num]
            except KeyError:
                if error_handler is None:
                    error_handler = codecs.lookup_error(errors)
                encode_error = UnicodeDecodeError(self.NAME, input, start_pos, next_pos, 'invalid sequence')
                replacement, next_pos = error_handler(encode_error)
                if replacement:
                    decode_buffer += replacement
            start_pos = next_pos
            num = 0
        return decode_buffer, next_pos


class IncrementalEncoder(codecs.IncrementalEncoder):

    def encode(self, input, final=False):
        return codecs.charmap_encode(input, self.errors, self._encoding_map)[0]


class IncrementalDecoder(codecs.IncrementalDecoder):

    def decode(self, input, final=False):
        return codecs.charmap_decode(input, self.errors, self._decode_map)[0]


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
    :return: CodecInfo for gsm03.38 codec
    :rtype: CodecInfo
    """
    return codecs.CodecInfo(
        name=Codec.NAME,
        encode=Codec().encode,
        decode=Codec().decode,
        incrementalencoder=IncrementalEncoder,
        incrementaldecoder=IncrementalDecoder,
        streamwriter=StreamWriter,
        streamreader=StreamReader,
    )


def find_gsm0338(encoding):
    """
    Return codec info for 'gsm03.38'
    :param str encoding: name of the searched encoding
    :rtype: CodecInfo
    """
    if encoding.lower() == Codec.NAME:
        return get_codec_info()
    return None
