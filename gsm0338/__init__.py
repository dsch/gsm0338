import codecs

__all__ = ["Codec"]

# Codec APIs


class Codec(codecs.Codec):

    def encode(self, input, errors='strict'):
        buffer = ""
        for c in input:
            num = encoding_map[ord(c)]
            if num & 0xff00:
                buffer += '\x1b'
            buffer += chr(num & 0xff)
        return (buffer, len(buffer))

    def decode(self, input, errors='strict'):
        buffer = u""
        num = 0
        for c in input:
            num |= ord(c)
            if num == 0x1b:
                num <<= 8
                continue

            buffer += unichr(decoding_map[num])
            num = 0
        return (buffer, len(buffer))


class IncrementalEncoder(codecs.IncrementalEncoder):

    def encode(self, input, final=False):
        return codecs.charmap_encode(input, self.errors, encoding_map)[0]


class IncrementalDecoder(codecs.IncrementalDecoder):

    def decode(self, input, final=False):
        return codecs.charmap_decode(input, self.errors, decoding_map)[0]


class StreamWriter(Codec, codecs.StreamWriter):
    pass


class StreamReader(Codec, codecs.StreamReader):
    pass


# encodings module API
def getregentry():
    return codecs.CodecInfo(
        name='gsm03.38',
        encode=Codec().encode,
        decode=Codec().decode,
        incrementalencoder=IncrementalEncoder,
        incrementaldecoder=IncrementalDecoder,
        streamwriter=StreamWriter,
        streamreader=StreamReader,
    )


decoding_map = codecs.make_identity_dict(range(127))
decoding_map.update({
    0x00: 0x0040,  # COMMERCIAL AT
    # (0x00, 0x0000), #NULL (see note above)
    0x01: 0x00A3,  # POUND SIGN
    0x02: 0x0024,  # DOLLAR SIGN
    0x03: 0x00A5,  # YEN SIGN
    0x04: 0x00E8,  # LATIN SMALL LETTER E WITH GRAVE
    0x05: 0x00E9,  # LATIN SMALL LETTER E WITH ACUTE
    0x06: 0x00F9,  # LATIN SMALL LETTER U WITH GRAVE
    0x07: 0x00EC,  # LATIN SMALL LETTER I WITH GRAVE
    0x08: 0x00F2,  # LATIN SMALL LETTER O WITH GRAVE
    #0x09: 0x00E7,  # LATIN SMALL LETTER C WITH CEDILLA
    0x09: 0x00C7, #LATIN CAPITAL LETTER C WITH CEDILLA (see note above)
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
    # ESCAPE TO EXTENSION TABLE (or displayed as NBSP, see note above)
    # 0x1B: 0x00A0,
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


# 0x41	0x0391	#	GREEK CAPITAL LETTER ALPHA
# 0x42	0x0392	#	GREEK CAPITAL LETTER BETA
# 0x45	0x0395	#	GREEK CAPITAL LETTER EPSILON
# 0x48	0x0397	#	GREEK CAPITAL LETTER ETA
# 0x49	0x0399	#	GREEK CAPITAL LETTER IOTA
# 0x4B	0x039A	#	GREEK CAPITAL LETTER KAPPA
# 0x4D	0x039C	#	GREEK CAPITAL LETTER MU
# 0x4E	0x039D	#	GREEK CAPITAL LETTER NU
# 0x4F	0x039F	#	GREEK CAPITAL LETTER OMICRON
# 0x50	0x03A1	#	GREEK CAPITAL LETTER RHO
# 0x54	0x03A4	#	GREEK CAPITAL LETTER TAU
# 0x58	0x03A7	#	GREEK CAPITAL LETTER CHI
# 0x59	0x03A5	#	GREEK CAPITAL LETTER UPSILON
# 0x5A	0x0396	#	GREEK CAPITAL LETTER ZETA


encoding_map = codecs.make_encoding_map(decoding_map)
