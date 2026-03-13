# API Reference

## normalize Function

::: email_normalize.normalize

## Normalizer Class

::: email_normalize.Normalizer

## Result Class

::: email_normalize.Result

## MXRecords Type

::: email_normalize.MXRecords

A type alias for a list of tuples containing the priority and host name for
each record returned during the MX lookup.

```python
list[tuple[int, str]]
```

**Example:**

```python
[
    (5, 'gmail-smtp-in.l.google.com'),
    (10, 'alt1.gmail-smtp-in.l.google.com'),
    (20, 'alt2.gmail-smtp-in.l.google.com'),
    (30, 'alt3.gmail-smtp-in.l.google.com'),
    (40, 'alt4.gmail-smtp-in.l.google.com'),
]
```
