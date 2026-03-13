# email-normalize

`email-normalize` is a Python 3 library for returning a normalized email-address
stripping mailbox provider specific behaviors such as "Plus addressing"
(foo+bar@gmail.com).

The email-normalize API has two primary components: a single function,
`email_normalize.normalize` and the `email_normalize.Normalizer`
class. Both use Python's `asyncio` library.

The `normalize` function is intended for use in non-async applications and the
`Normalizer` is intended for async applications. `normalize` uses `Normalizer`
under the hood.

## Installation

email-normalize is available via the [Python Package Index](https://pypi.org).

```bash
pip install email-normalize
```

## Example

```python
import email_normalize

result = email_normalize.normalize('f.o.o+bar@gmail.com')
print(result.normalized_address)  # foo@gmail.com
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
