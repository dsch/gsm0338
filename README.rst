gsm0338
=======
.. image:: https://travis-ci.org/dsch/gsm0338.svg?branch=master
    :target: https://travis-ci.org/dsch/gsm0338

Python Codec for 3GPP TS 23.038 / ETSI GSM 03.38


Examples
--------
Decode GSM 03.38 encoded bytes:

    >>> import gsm0338
    >>> b'\x1b(\x1b)'.decode('gsm03.38')
    u'{}'

Encode bytes in GSM 03.38:

    >>> import gsm0338
    >>> u'{}'.encode('gsm03.38')
    b'\x1b(\x1b)'


How it works
------------
The codec implements the encoding and decoding methods in the stateless codecs.Codec class.
With loading the module the codec get's automatically registered.


Mapping source
--------------
`3GPP TS 23.038 version 13.0.0 Release 13`_

.. _3GPP TS 23.038 version 13.0.0 Release 13: http://www.etsi.org/deliver/etsi_ts/123000_123099/123038/13.00.00_60/ts_123038v130000p.pdf


3GPP TS 23.038 Rel-13: Alphabets and language-specific information
http://www.3gpp.org/dynareport/23038.htm
