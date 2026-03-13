# email-normalize

`email-normalize` is a Python 3 library for returning a normalized email-address
stripping mailbox provider specific behaviors such as "Plus addressing"
(foo+bar@gmail.com).

![Version](https://img.shields.io/pypi/v/email-normalize.svg?)
![Status](https://github.com/gmr/email-normalize/workflows/Testing/badge.svg?)
![Coverage](https://img.shields.io/codecov/c/github/gmr/email-normalize.svg?)
![License](https://img.shields.io/pypi/l/email-normalize.svg?)

## Example

```python
import email_normalize

# Returns ``foo@gmail.com``
normalized = email_normalize.normalize('f.o.o+bar@gmail.com')
```

## Currently Supported Mailbox Providers

- Apple
- Fastmail
- Google
- Microsoft
- ProtonMail
- Rackspace
- Yahoo
- Yandex
- Zoho

## Python Versions Supported

3.11+
