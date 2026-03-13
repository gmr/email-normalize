# email-normalize

A Python 3.11+ library for normalizing email addresses by stripping
mailbox-provider-specific behaviors such as plus addressing
(`foo+bar@gmail.com`) and period ignoring (`f.o.o@gmail.com`).

![Version](https://img.shields.io/pypi/v/email-normalize.svg?)
![Status](https://github.com/gmr/email-normalize/workflows/Testing/badge.svg?)
![Coverage](https://img.shields.io/codecov/c/github/gmr/email-normalize.svg?)
![License](https://img.shields.io/pypi/l/email-normalize.svg?)

## Installation

```bash
pip install email-normalize
```

## Usage

### Synchronous

```python
import email_normalize

result = email_normalize.normalize('f.o.o+bar@gmail.com')
print(result.normalized_address)  # foo@gmail.com
print(result.mailbox_provider)    # Google
print(result.mx_records)          # [(5, 'gmail-smtp-in.l.google.com'), ...]
```

### Async

For use within an asyncio application, use the `Normalizer` class directly:

```python
import asyncio

import email_normalize


async def main():
    normalizer = email_normalize.Normalizer()
    result = await normalizer.normalize('f.o.o+bar@gmail.com')
    print(result.normalized_address)

asyncio.run(main())
```

The `Normalizer` maintains a LFRU cache of MX lookups, making it efficient
for batch processing.

### Without DNS Lookups

Use `skip_dns=True` to normalize against well-known domains without
performing MX record lookups:

```python
result = email_normalize.normalize('user+tag@gmail.com', skip_dns=True)
```

This mode uses a static domain map and will not detect providers for
custom domains.

## Normalization Rules

| Provider   | Plus Addressing | Strip Periods | Local Part as Hostname |
|------------|:---------------:|:-------------:|:----------------------:|
| Apple      | x               |               |                        |
| Fastmail   | x               |               | x                      |
| Google     | x               | x             |                        |
| Microsoft  | x               |               |                        |
| ProtonMail | x               |               |                        |
| Rackspace  | x               |               |                        |
| Yahoo      |                 |               |                        |
| Yandex     | x               |               |                        |
| Zoho       | x               |               |                        |

- **Plus Addressing**: Strips everything after `+` in the local part
- **Strip Periods**: Removes `.` from the local part
- **Local Part as Hostname**: Extracts the subdomain as the local part (Fastmail custom domains)

## Documentation

Full documentation is available at [gmr.github.io/email-normalize](https://gmr.github.io/email-normalize/).
