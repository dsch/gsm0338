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
`3GPP TS 23.038 version 12.0.0 Release 12`_

.. _3GPP TS 23.038 version 12.0.0 Release 12: http://www.etsi.org/deliver/etsi_ts/123000_123099/123038/12.00.00_60/ts_123038v120000p.pdf
