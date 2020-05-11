MXRecords Type
==============

.. data:: email_normalize.MXRecords

    A typing alias for list of tuples containing the priority and host name for
    each record returned during the MX lookup.

    .. code-block:: python

        typing.List[typing.Tuple[int, str]]

**Example**

.. code-block:: python

    [
        (5, 'gmail-smtp-in.l.google.com'),
        (10, 'alt1.gmail-smtp-in.l.google.com'),
        (20, 'alt2.gmail-smtp-in.l.google.com'),
        (30, 'alt3.gmail-smtp-in.l.google.com'),
        (40, 'alt4.gmail-smtp-in.l.google.com')
    ]
