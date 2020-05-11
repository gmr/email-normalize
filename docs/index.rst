email-normalize
===============
``email-normalize`` is a Python 3 library for returning a normalized email-address
stripping mailbox provider specific behaviors such as "Plus addressing"
(foo+bar@gmail.com).

The email-normalize API has two primary components: a single function,
:func:`email_normalize.normalize` and the :class:`email_normalize.Normalizer`
class. Both use Python's :py:mod:`asyncio` library.

The :func:`~email_normalize.normalize` function is intended for
use in non-async applications and the :class:`~email_normalize.Normalizer` is
intended for async applications. :func:`~email_normalize.normalize` uses
:class:`~email_normalize.Normalizer` under the hood.

Documentation
-------------
.. toctree::
   :maxdepth: 1

   normalize
   normalizer
   mxrecords
   result

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

Installation
------------
email-normalize is available via the `Python Package Index <https://pypi.org>`_.

.. code::

    pip3 install email-normalize

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
