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
:class:`~email_normalize.Normalizer` under the covers.

Documentation
-------------
.. toctree::
   :maxdepth: 1

   normalize
   normalizer
   mxrecords
   result


Installation
------------
email-normalize is available via the `Python Package Index <https://pypi.org>`_.

.. code::

    pip3 install email-normalize

License
-------

.. code-block:: none

    Copyright (c) 2015-2020 Gavin M. Roy
    All rights reserved.

    Redistribution and use in source and binary forms, with or without modification,
    are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice, this
      list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright notice,
      this list of conditions and the following disclaimer in the documentation
      and/or other materials provided with the distribution.
    * Neither the name of the copyright holder nor the names of its contributors may
      be used to endorse or promote products derived from this software without
      specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
    ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
    WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
    IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
    INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
    BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
    DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
    OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
    ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
