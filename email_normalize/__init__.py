"""
email-normalize
===============

Library for returning a normalized email-address stripping mailbox provider
specific behaviors such as "Plus addressing" (foo+bar@gmail.com).

"""
import asyncio
import copy
import dataclasses
import logging
import operator
import time
import typing
from email import utils

import aiodns
from aiodns import error

from email_normalize import providers

LOGGER = logging.getLogger(__name__)

MXRecords = typing.List[typing.Tuple[int, str]]


class CachedItem:
    """Used to represent a cached lookup for implementing a LFRU cache"""
    __slots__ = ['cached_at', 'hits', 'last_access', 'mx_records', 'ttl']

    def __init__(self, mx_records: MXRecords, ttl: int):
        self.cached_at = time.monotonic()
        self.hits = 0
        self.last_access: float = 0.0
        self.mx_records = mx_records
        self.ttl = ttl

    @property
    def expired(self):
        return (time.monotonic() - self.cached_at) > self.ttl


@dataclasses.dataclass(frozen=True)
class Result:
    """Instances of the :class:`~email_normalize.Result` class contain data
    from the email normalization process.

    :param address: The address that was normalized
    :type address: str
    :param normalized_address: The normalized version of the address
    :type normalized_address: str
    :param mx_records: A list of tuples representing the priority and host of
        the MX records found for the email address. If empty, indicates a
        failure to lookup the domain part of the email address.
    :type mx_records: :data:`~email_normalize.MXRecords`
    :param mailbox_provider: String that represents the mailbox provider name
        - is `None` if the mailbox provider could not be detected or
        was unsupported.
    :type mailbox_provider: str

    .. note:: If during the normalization process the MX records could not be
        resolved, the ``mx_records`` attribute will be an empty :class:`list`
        and the ``mailbox_provider`` attribute will be :data:`None`.

    **Example**

    .. code-block:: python

        @dataclasses.dataclass(frozen=True)
        class Result:
            address = 'Gavin.M.Roy+ignore-spam@gmail.com'
            normalized_address = 'gavinmroy@gmail.com'
            mx_records =     [
                (5, 'gmail-smtp-in.l.google.com'),
                (10, 'alt1.gmail-smtp-in.l.google.com'),
                (20, 'alt2.gmail-smtp-in.l.google.com'),
                (30, 'alt3.gmail-smtp-in.l.google.com'),
                (40, 'alt4.gmail-smtp-in.l.google.com')
            ]
            mailbox_provider = 'Gmail'

    """
    address: str
    normalized_address: str
    mx_records: MXRecords
    mailbox_provider: typing.Optional[str] = None


class Normalizer:
    """Singleton class for normalizing an email address and resolving MX
    records.

    Normalization is processed by splitting the local and domain parts of the
    email address and then performing DNS resolution for the MX records
    associated with the domain part of the address. The MX records are
    processed against a set of mailbox provider specific rules. If a match
    is found for the MX record hosts, the rules are applied to the email
    address.

    This class implements a least frequent recently used cache that respects
    the DNS TTL returned when performing MX lookups.

    **Usage Example**

    .. code-block:: python

        async def normalize(email_address: str) -> email_normalize.Result:
            normalizer = email_normalize.Normalizer()
            return await normalizer.normalize('foo@bar.io')

    :param name_servers: Optional list of hostnames to use for DNS resolution
    :type name_servers: list(str) or None
    :param int cache_limit: The maximum number of domain results that are
        cached. Defaults to `1024`.

    :param bool cache_failures: Toggle the behavior of caching DNS resolution
        failures for a given domain. When enabled, failures will be cached
        for `failure_ttl` seconds. Defaults to `True`.
    :param int failure_ttl: Duration in seconds to cache DNS failures. Only
        works when `cache_failures` is set to `True`. Defaults to `300`
        seconds.

    """
    _instance = None

    def __new__(cls,
                name_servers: typing.Optional[typing.List[str]] = None,
                cache_limit: int = 1024,
                cache_failures: bool = True,
                failure_ttl: int = 300) \
            -> 'Normalizer':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._resolver = aiodns.DNSResolver(name_servers)
        cls.cache: typing.Dict[str, CachedItem] = {}
        cls.cache_failures = cache_failures
        cls.cache_limit = cache_limit
        cls.failure_ttl = failure_ttl
        return cls._instance

    async def mx_records(self, domain_part: str) -> MXRecords:
        """Resolve MX records for a domain returning a list of tuples with the
        MX priority and value.

        :param domain_part: The domain to resolve MX records for
        :type domain_part: str
        :rtype:  :data:`~email_normalize.MXRecords`

        """
        if self._skip_cache(domain_part):
            try:
                records = await self._resolver.query(domain_part, 'MX')
            except error.DNSError as err:
                LOGGER.debug('Failed to resolve %r: %s', domain_part, err)
                if not self.cache_failures:
                    return []
                mx_records, ttl = [], self.failure_ttl
            else:
                mx_records = [(r.priority, r.host) for r in records]
                ttl = min(r.ttl for r in records) if records else []

            # Prune the cache if it's >= the limit, finding least used, oldest
            if len(self.cache.keys()) >= self.cache_limit:
                del self.cache[sorted(
                    self.cache.items(),
                    key=lambda i: (i[1].hits, i[1].last_access))[0][0]]

            self.cache[domain_part] = CachedItem(
                sorted(mx_records, key=operator.itemgetter(0, 1)), ttl)

        self.cache[domain_part].hits += 1
        self.cache[domain_part].last_access = time.monotonic()
        return copy.deepcopy(self.cache[domain_part].mx_records)

    async def normalize(self, email_address: str) -> Result:
        """Return a :class:`~email_normalize.Result` instance containing the
        original address, the normalized address, the MX records found, and
        the detected mailbox provider.

        .. note:: If the MX records could not be resolved, the ``mx_records``
            attribute of the result will be an empty :class:`list` and the
            ``mailbox_provider`` will be :data:`None`.

        :param email_address: The address to normalize
        :rtype: :class:`~email_normalize.Result`

        """
        address = utils.parseaddr(email_address)
        local_part, domain_part = address[1].lower().split('@')
        mx_records = await self.mx_records(domain_part)
        provider = self._lookup_provider(mx_records)
        if provider:
            if provider.Flags & providers.Rules.LOCAL_PART_AS_HOSTNAME:
                local_part, domain_part = self._local_part_as_hostname(
                    local_part, domain_part)
            if provider.Flags & providers.Rules.STRIP_PERIODS:
                local_part = local_part.replace('.', '')
            if provider.Flags & providers.Rules.PLUS_ADDRESSING:
                local_part = local_part.split('+')[0]
            if provider.Flags & providers.Rules.DASH_ADDRESSING:
                local_part = local_part.split('-')[0]
        return Result(email_address, '@'.join([local_part, domain_part]),
                      mx_records, provider.__name__ if provider else None)

    @staticmethod
    def _local_part_as_hostname(local_part: str,
                                domain_part: str) -> typing.Tuple[str, str]:
        domain_segments = domain_part.split('.')
        if len(domain_segments) > 2:
            local_part = domain_segments[0]
            domain_part = '.'.join(domain_segments[1:])
        return local_part, domain_part

    @staticmethod
    def _lookup_provider(mx_records: typing.List[typing.Tuple[int, str]]) \
            -> typing.Optional[providers.MailboxProvider]:
        for priority, host in mx_records:
            for provider in providers.Providers:
                for domain in provider.MXDomains:
                    if host.endswith(domain):
                        return provider

    def _skip_cache(self, domain: str) -> bool:
        if domain not in self.cache:
            return True
        elif self.cache[domain].expired:
            del self.cache[domain]
            return True
        return False


def normalize(email_address: str) -> Result:
    """Normalize an email address

    This method abstracts the :mod:`asyncio` base for this library and
    provides a blocking function. If you intend to use this library as part of
    an :mod:`asyncio` based application, it is recommended that you use
    the :meth:`~email_normalize.Normalizer.normalize` instead.

    .. note:: If the MX records could not be resolved, the ``mx_records``
        attribute of the result will be an empty :class:`list` and the
        ``mailbox_provider`` attribute will be :data:`None`.

    **Usage Example**

    .. code-block:: python

        import email_normalize

        result = email_normalize.normalize('foo@bar.io')

    :param email_address: The address to normalize

    """
    loop = asyncio.get_event_loop()
    normalizer = Normalizer()
    return loop.run_until_complete(normalizer.normalize(email_address))
