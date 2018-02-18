gsm0338
=======
.. image:: http://img.shields.io/pypi/v/gsm0338.svg
   :target: https://pypi.python.org/pypi/gsm0338

.. image:: https://travis-ci.org/dsch/gsm0338.svg?branch=master
    :target: https://travis-ci.org/dsch/gsm0338

.. image:: http://img.shields.io/badge/license-MIT-green.svg
   :target: https://github.com/dsch/gsm0338/blob/master/LICENSE

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
`3GPP TS 23.038 version 14.0.0 Release 14`_

.. _3GPP TS 23.038 version 14.0.0 Release 14: http://www.etsi.org/deliver/etsi_ts/123000_123099/123038/14.00.00_60/ts_123038v140000p.pdf


3GPP TS 23.038 Rel-14: Alphabets and language-specific information
http://www.3gpp.org/dynareport/23038.htm
