gsm0338
=======
.. image:: http://img.shields.io/pypi/v/gsm0338.svg
   :target: https://pypi.python.org/pypi/gsm0338

.. image:: https://codecov.io/gh/dsch/gsm0338/branch/master/graphs/badge.svg
    :target: https://codecov.io/gh/dsch/gsm0338/branch/master

.. image:: http://img.shields.io/badge/license-MIT-green.svg
   :target: https://github.com/dsch/gsm0338/blob/master/LICENSE

.. image:: https://results.pre-commit.ci/badge/github/dsch/gsm0338/master.svg
   :target: https://results.pre-commit.ci/latest/github/dsch/gsm0338/master
   :alt: pre-commit.ci status

Python Codec for 3GPP TS 23.038 / ETSI GSM 03.38

.. note:: This codec doesn't cover character packing as in chapter 6.1.2 of the GSM standard.
          The byte array has already to be split into octets.

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
`3GPP TS 23.038 version 15.0.0 Release 15`_

.. _3GPP TS 23.038 version 15.0.0 Release 15: https://www.etsi.org/deliver/etsi_ts/123000_123099/123038/15.00.00_60/ts_123038v150000p.pdf


3GPP TS 23.038 Rel-15: Alphabets and language-specific information
http://www.3gpp.org/dynareport/23038.htm

Development
-----------
Use `Poetry <https://python-poetry.org/>`_ to install project dependencies.

    poetry install
