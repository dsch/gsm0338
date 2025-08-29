import codecs
import unicodedata

from .charset import BASIC_CHARACTER_SET, BASIC_CHARACTER_SET_EXTENSION


# Codec APIs
class Codec(codecs.Codec):
    """
    Stateless encoder and decoder for GSM 03.38
    """

    NAME = "gsm03.38"
    __ESCAPE = 0x1B

    def __init__(
        self,
        locking_shift_decode_map=BASIC_CHARACTER_SET,
        single_shift_decode_map=BASIC_CHARACTER_SET_EXTENSION,
    ):
        self._decode_map = dict(
            [
                (key, unicodedata.lookup(name))
                for key, name in locking_shift_decode_map.items()
            ]
        )
        self._decode_map.update(
            dict(
                ((self.__ESCAPE << 8 | key), unicodedata.lookup(name))
                for key, name in single_shift_decode_map.items()
            )
        )

        self._encoding_map = codecs.make_encoding_map(self._decode_map)

    # noinspection PyShadowingBuiltins
    def encode(self, input, errors="strict"):
        """
        Encode string to byte array
        :param str input: string (unicode) object to convert to byte array
        :param str errors: defines the error handling to apply
        :return: returns a tuple (output object, length consumed)
        :rtype: (bytes,int)
        """

        error_handler = None  # cache for error handler
        encode_buffer = b""
        pos = 0
        input_length = len(input)
        while pos < input_length:
            try:
                encode_buffer += self.__encode_character(input[pos])
                pos += 1
            except KeyError:
                if error_handler is None:
                    error_handler = codecs.lookup_error(errors)
                encode_error = UnicodeEncodeError(
                    self.NAME, input, pos, pos + 1, "character not mapped"
                )
                replacement, pos = error_handler(encode_error)
                if isinstance(replacement, str):
                    encode_buffer += b"".join(
                        [self.__encode_character(c) for c in replacement]
                    )
                else:
                    encode_buffer += replacement
        return encode_buffer, pos

    def __encode_character(self, character):
        append_buffer = b""
        num = self._encoding_map[character]
        if num & 0xFF00:
            append_buffer += bytes((self.__ESCAPE,))
        append_buffer += bytes((num & 0xFF,))
        return append_buffer

    # noinspection PyShadowingBuiltins
    def decode(self, input, errors="strict"):
        """
        Decode byte array to string
        :param bytes input: byte array to convert to unicode string
        :param str errors: defines the error handling to apply
        :return: returns a tuple (output object, length consumed)
        :rtype: (str,int)
        """

        error_handler = None  # cache for error handler
        decode_buffer = ""

        start_pos = 0
        next_pos = 0
        num = 0
        input_length = len(input)
        while next_pos < input_length:
            try:
                num |= input[next_pos]
                next_pos += 1
                if num == self.__ESCAPE:
                    num <<= 8
                    continue
                decode_buffer += self._decode_map[num]
            except KeyError:
                if error_handler is None:
                    error_handler = codecs.lookup_error(errors)
                encode_error = UnicodeDecodeError(
                    self.NAME, input, start_pos, next_pos, "invalid sequence"
                )
                replacement, next_pos = error_handler(encode_error)
                if replacement:
                    decode_buffer += replacement
            start_pos = next_pos
            num = 0
        return decode_buffer, next_pos

    # encodings module API
    @classmethod
    def get_codec_info(cls):
        """
        encodings module API
        :return: CodecInfo for gsm03.38 codec
        :rtype: CodecInfo
        """
        return codecs.CodecInfo(
            name=cls.NAME,
            encode=cls().encode,
            decode=cls().decode,
            incrementalencoder=IncrementalEncoder,
            incrementaldecoder=IncrementalDecoder,
            streamwriter=StreamWriter,
            streamreader=StreamReader,
        )


class IncrementalEncoder(codecs.IncrementalEncoder):
    # noinspection PyShadowingBuiltins
    def encode(self, input, final=False):
        return codecs.charmap_encode(input, self.errors, self._encoding_map)[0]


class IncrementalDecoder(codecs.IncrementalDecoder):
    # noinspection PyShadowingBuiltins
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


@codecs.register
def find_gsm0338(encoding):
    """
    Return codec info for 'gsm03.38'
    :param str encoding: name of the searched encoding
    :rtype: CodecInfo
    """
    if encoding.lower() == Codec.NAME:
        return Codec.get_codec_info()
