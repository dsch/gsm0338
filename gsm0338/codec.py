import codecs
import unicodedata

from six import byte2int, int2byte

from .charset import BASIC_CHARACTER_SET, BASIC_CHARACTER_SET_EXTENSION


# Codec APIs
class Codec(codecs.Codec):
    """
    Stateless encoder and decoder for GSM 03.38
    """

    NAME = 'gsm03.38'
    __ESCAPE = 0x1b
    __UNICODE_LOOKUP_FALLBACK = {
        'LINE-FEED': u'\x0A',
        'FORM FEED': u'\x0C',
        'CARRIAGE RETURN': u'\x0D',
        'ESCAPE': u'\x1B',
    }

    def __init__(self, locking_shift_decode_map=None, single_shift_decode_map=None):
        if locking_shift_decode_map is None:
            locking_shift_decode_map = BASIC_CHARACTER_SET
        if single_shift_decode_map is None:
            single_shift_decode_map = BASIC_CHARACTER_SET_EXTENSION

        self._decode_map = dict(
            [(key, self.__unicode_lookup(name)) for key, name in locking_shift_decode_map.items()])
        self._decode_map.update(
            dict(((self.__ESCAPE << 8 | key), self.__unicode_lookup(name))
                 for key, name in single_shift_decode_map.items()))

        self._encoding_map = codecs.make_encoding_map(self._decode_map)

    @staticmethod
    def __unicode_lookup(name):
        try:
            return unicodedata.lookup(name)
        except KeyError:
            # this error handling is only used for python 2.7
            return Codec.__UNICODE_LOOKUP_FALLBACK[name]

    def encode(self, input, errors='strict'):
        """
        Encode string to byte array
        :param str input: string (unicode) object to convert to byte array
        :param str errors: defines the error handling to apply
        :return: returns a tuple (output object, length consumed)
        :rtype: (bytes,int)
        """
        encode_buffer = b''
        consumed = 0
        for character in input:
            consumed += 1
            num = None
            try:
                num = self._encoding_map[character]
            except KeyError:
                if errors == 'replace':
                    num = 0x3f  # question mark
                elif errors == 'ignore':
                    pass
                else:
                    raise ValueError("'%s' codec can't encode character %r in position %d" %
                                     (self.NAME, character, consumed - 1))
            if num is not None:
                if num & 0xff00:
                    encode_buffer += int2byte(self.__ESCAPE)
                encode_buffer += int2byte(num & 0xff)
        return encode_buffer, consumed

    def decode(self, input, errors='strict'):
        """
        Decode byte array to string
        :param bytes input: byte array to convert to unicode string
        :param str errors: defines the error handling to apply
        :return: returns a tuple (output object, length consumed)
        :rtype: (str,int)
        """
        decode_buffer = u""
        consumed = 0

        num = 0
        for value in input:
            consumed += 1
            num |= byte2int([value])
            if num == self.__ESCAPE:
                num <<= 8
                continue
            try:
                decode_buffer += self._decode_map[num]
            except KeyError as ex:
                if errors == 'replace':
                    decode_buffer += u'\ufffd'
                elif errors == 'ignore':
                    pass
                else:
                    if num & (self.__ESCAPE << 8):
                        raise ValueError("'%s' codec can't decode byte 0x%x in position %d" %
                                         (self.NAME, ex.args[0] & 0xff, consumed - 1))
                    else:
                        raise ValueError("'%s' codec can't decode byte 0x%x in position %d" %
                                         (self.NAME, ex.args[0], consumed - 1))
            num = 0
        return decode_buffer, consumed


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
