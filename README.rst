email-normalize
===============
Return a normalized email-address stripping ISP specific behaviors such as
"Plus addressing" (``foo+bar@gmail.com``). It will also parse out addresses that
are in the ``"Real Name" <address>`` format.

|Version| |Downloads| |Status| |Coverage| |CodeClimate| |License| |PythonVersions|

Example
-------

.. code:: python

    from email_normalize import normalize

    # Returns ``foo@gmail.com``
    normalized = normalize('f.o.o+bar@gmail.com')

.. |Version| image:: https://img.shields.io/pypi/v/email-normalize.svg?
   :target: https://pypi.python.org/pypi/email-normalize

.. |Status| image:: https://img.shields.io/travis/gmr/email-normalize.svg?
   :target: https://travis-ci.org/gmr/email-normalize

.. |Coverage| image:: https://img.shields.io/codecov/c/github/gmr/email-normalize.svg?
   :target: https://codecov.io/github/gmr/email-normalize?branch=master

.. |Downloads| image:: https://img.shields.io/pypi/dm/email-normalize.svg?
   :target: https://pypi.python.org/pypi/email-normalize

.. |License| image:: https://img.shields.io/github/license/gmr/email-normalize.svg?
   :target: https://github.com/gmr/email-normalize

.. |CodeClimate| image:: https://img.shields.io/codeclimate/github/gmr/email-normalize.svg?
   :target: https://codeclimate.com/github/gmr/email-normalize

.. |PythonVersions| image:: https://img.shields.io/pypi/pyversions/email-normalize.svg?
   :target: https://github.com/gmr/email-normalize
