email-normalize
===============
``email-normalize`` is a Python 3 library for returning a normalized email-address
stripping mailbox provider specific behaviors such as "Plus addressing"
(foo+bar@gmail.com).

|Version| |Status| |Coverage| |License|

Example
-------

.. code:: python

    import email_normalize

    # Returns ``foo@gmail.com``
    normalized = email_normalize.normalize('f.o.o+bar@gmail.com')

Currently Supported Mailbox Providers
-------------------------------------
- Apple
- Fastmail
- Google
- Microsoft
- ProtonMail
- Rackspace
- Yahoo
- Yandex
- Zoho

Documentation
-------------
http://email-normalize.readthedocs.org

Python Versions Supported
-------------------------
3.7+

.. |Version| image:: https://img.shields.io/pypi/v/email-normalize.svg?
   :target: https://pypi.python.org/pypi/email-normalize

.. |Status| image:: https://github.com/gmr/email-normalize/workflows/Testing/badge.svg?
   :target: https://github.com/gmr/email-normalize/actions?workflow=Testing
   :alt: Build Status

.. |Coverage| image:: https://img.shields.io/codecov/c/github/gmr/email-normalize.svg?
   :target: https://codecov.io/github/gmr/email-normalize?branch=master

.. |License| image:: https://img.shields.io/pypi/l/email-normalize.svg?
   :target: https://email-normalize.readthedocs.org
