gsm0338
=======
.. image:: https://travis-ci.org/dsch/gsm0338.svg?branch=master
    :target: https://travis-ci.org/dsch/gsm0338

Python Codec for ETSI GSM 03.38


Example
-------
Decode GSM 03.38 encoded bytes:

    >>> import gsm0338
    >>> b'\x1b(\x1b)'.decode('gsm0338')
    u'{}'


Mapping source
--------------
`GSM 03.38 to Unicode`_

**Exception:** Uppercase C-cedilla glyph at 0x09 as in ETSI GSM standard  


.. _GSM 03.38 to Unicode: ftp://ftp.unicode.org/Public/MAPPINGS/ETSI/GSM0338.TXT
