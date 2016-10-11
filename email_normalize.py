"""
email-normalize
===============
Return a normalized email-address stripping ISP specific behaviors such as
"Plus addressing" (foo+bar@gmail.com). It will also parse out addresses that
are in the ``"Real Name" <address>`` format.

Example
-------

.. code:: python

    from email_normalize import normalize

    # Returns ``foo@gmail.com``
    normalized = normalize('f.o.o+bar@gmail.com')


"""
import logging
from email import utils

from dns import resolver

LOGGER = logging.getLogger(__name__)

__version__ = '0.2.1'

FASTMAIL_DOMAINS = set(['fastmail.com', 'messagingengine.com', 'fastmail.fm'])
GMAIL_DOMAINS = set(['google.com', 'googlemail.com', 'gmail.com'])
MICROSOFT_DOMAINS = set(['hotmail.com', 'outlook.com', 'live.com'])
YAHOO_DOMAINS = set(['yahoodns.net', 'yahoo.com', 'ymail.com'])


def _get_mx_exchanges(domain):
    """Fetch the MX records for the specified domain

    :param str domain: The domain to get the MX records for
    :rtype: list

    """
    try:
        answer = resolver.query(domain, 'MX')
        return [str(record.exchange).lower()[:-1] for record in answer]
    except (resolver.NoAnswer, resolver.NoNameservers, resolver.NotAbsolute,
            resolver.NoRootSOA, resolver.NXDOMAIN, resolver.Timeout) as error:
        LOGGER.error('Error querying MX for %s: %r', domain, error)
        return []


def _domain_check(domain, domain_list, resolve):
    """Returns ``True`` if the ``domain`` is serviced by the ``domain_list``.

    :param str domain: The domain to check
    :param list domain_list: The domains to check for
    :param bool resolve: Resolve the domain
    :rtype: bool

    """
    if domain in domain_list:
        return True
    if resolve:
        for exchange in _get_mx_exchanges(domain):
            for value in domain_list:
                if exchange.endswith(value):
                    return True
    return False


def _is_fastmail(domain, resolve):
    """Returns ``True`` if the domain is hosted by FastMail.com

    :param str domain: The domain to check to see for fastmail.com hosting
    :param bool resolve: Resolve the domain
    :rtype: bool

    """
    return _domain_check(domain, FASTMAIL_DOMAINS, resolve)


def _is_gmail(domain, resolve):
    """Returns ``True`` if the domain is hosted by Google

    :param str domain: The domain to check to see for gmail hosting
    :param bool resolve: Resolve the domain
    :rtype: bool

    """
    return _domain_check(domain, GMAIL_DOMAINS, resolve)


def _is_yahoo(domain, resolve):
    """Returns ``True`` if the domain is hosted by Yahoo

    :param str domain: The domain to check to see for yahoo hosting
    :param bool resolve: Resolve the domain
    :rtype: bool

    """
    return _domain_check(domain, YAHOO_DOMAINS, resolve)


def normalize(email_address, resolve=True):
    """Return the normalized email address, removing

    :param str email_address: The normalized email address
    :param bool resolve: Resolve the domain
    :rtype: str

    """
    address = utils.parseaddr(email_address)
    local_part, domain_part = address[1].lower().split('@')

    # Plus addressing is supported by Microsoft domains and FastMail
    if domain_part in MICROSOFT_DOMAINS:
        if '+' in local_part:
            local_part = local_part.split('+')[0]

    # GMail supports plus addressing and throw-away period delimiters
    elif _is_gmail(domain_part, resolve):
        local_part = local_part.replace('.', '').split('+')[0]

    # Yahoo domain handling of - is like plus addressing
    elif _is_yahoo(domain_part, resolve):
        if '-' in local_part:
            local_part = local_part.split('-')[0]

    # FastMail has domain part username aliasing and plus addressing
    elif _is_fastmail(domain_part, resolve):
        domain_segments = domain_part.split('.')
        if len(domain_segments) > 2:
            local_part = domain_segments[0]
            domain_part = '.'.join(domain_segments[1:])
        elif '+' in local_part:
            local_part = local_part.split('+')[0]

    return '@'.join([local_part, domain_part])
