email-normalize
===============
Library for returning a normalized email-address stripping mailbox provider
specific behaviors such as "Plus addressing" (foo+bar@gmail.com).

|Version| |Status| |Coverage| |License|

Example
-------

.. code:: python

    import email_normalize

    # Returns ``foo@gmail.com``
    normalized = email_normalize.normalize('f.o.o+bar@gmail.com')

Documentation
-------------
http://email-normalize.readthedocs.org

License
-------
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
