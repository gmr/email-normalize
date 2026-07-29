"""email-normalize
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
from email import utils

import aiodns
import tldextract
from aiodns import error

from email_normalize import providers

LOGGER = logging.getLogger(__name__)

MXRecords = list[tuple[int, str]]

_tld_extract = tldextract.TLDExtract(
    suffix_list_urls=(), cache_dir=None, fallback_to_snapshot=True
)

cache: dict[str, 'CachedItem'] = {}


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
    """Contains data from the email normalization process.

    Attributes:
        address: The address that was normalized.
        normalized_address: The normalized version of the address.
        mx_records: A list of tuples representing the priority and host
            of the MX records found for the email address. If empty,
            indicates a failure to lookup the domain part.
        mailbox_provider: The mailbox provider name, or ``None`` if
            the provider could not be detected or was unsupported.

    """

    address: str
    normalized_address: str
    mx_records: MXRecords
    mailbox_provider: str | None = None


class Normalizer:
    """Class for normalizing an email address and resolving MX records.

    Normalization is processed by splitting the local and domain parts of the
    email address and then performing DNS resolution for the MX records
    associated with the domain part of the address. The MX records are
    processed against a set of mailbox provider specific rules. If a match
    is found for the MX record hosts, the rules are applied to the email
    address.

    This class implements a least frequent recently used cache that respects
    the DNS TTL returned when performing MX lookups. Data is cached at the
    **module** level.

    Args:
        name_servers: Optional list of hostnames to use for DNS
            resolution.
        cache_limit: The maximum number of domain results that are
            cached. Defaults to ``1024``.
        cache_failures: Toggle the behavior of caching DNS resolution
            failures for a given domain. When enabled, failures will be
            cached for ``failure_ttl`` seconds. Defaults to ``True``.
        failure_ttl: Duration in seconds to cache DNS failures. Only
            works when ``cache_failures`` is set to ``True``. Defaults
            to ``300`` seconds.

    """

    def __init__(
        self,
        name_servers: list[str] | None = None,
        cache_limit: int = 1024,
        cache_failures: bool = True,
        failure_ttl: int = 300,
        skip_dns: bool = False,
    ) -> None:
        self._skip_dns = skip_dns
        if not skip_dns:
            self._resolver = aiodns.DNSResolver(name_servers)
        self.cache_failures = cache_failures
        self.cache_limit = cache_limit
        self.failure_ttl = failure_ttl

    async def mx_records(self, domain_part: str) -> MXRecords:
        """Resolve MX records for a domain.

        Returns a list of tuples with the MX priority and value.

        Args:
            domain_part: The domain to resolve MX records for.

        """
        if self._skip_dns:
            return []
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
                ttl = min(
                    (r.ttl for r in records if r.ttl >= 0),
                    default=self.failure_ttl,
                )

            # Prune the cache if over the limit
            if len(cache.keys()) >= self.cache_limit:
                key_to_prune = sorted(
                    cache.items(), key=lambda i: (i[1].hits, i[1].last_access)
                )[0][0]
                LOGGER.debug('Pruning cache of %s', key_to_prune)
                del cache[key_to_prune]

            cache[domain_part] = CachedItem(
                sorted(mx_records, key=operator.itemgetter(0, 1)), ttl
            )

        cache[domain_part].hits += 1
        cache[domain_part].last_access = time.monotonic()
        return copy.deepcopy(cache[domain_part].mx_records)

    async def normalize(self, email_address: str) -> Result:
        """Normalize an email address.

        Returns a ``Result`` containing the original address, the
        normalized address, the MX records found, and the detected
        mailbox provider.

        Args:
            email_address: The address to normalize.

        """
        address = utils.parseaddr(email_address)
        local_part, domain_part = address[1].lower().split('@')
        if self._skip_dns:
            mx_records = []
            provider = self._lookup_provider_by_domain(domain_part)
        else:
            mx_records = await self.mx_records(domain_part)
            provider = self._lookup_provider(mx_records)
        if provider:
            if provider.Flags & providers.Rules.LOCAL_PART_AS_HOSTNAME:
                local_part, domain_part = self._local_part_as_hostname(
                    local_part, domain_part
                )
            if provider.Flags & providers.Rules.STRIP_PERIODS and (
                not provider.StripPeriodDomains
                or domain_part in provider.StripPeriodDomains
            ):
                local_part = local_part.replace('.', '')
            if provider.Flags & providers.Rules.PLUS_ADDRESSING:
                local_part = local_part.split('+')[0]
            domain_part = provider.CanonicalDomains.get(
                domain_part, domain_part
            )
        return Result(
            email_address,
            f'{local_part}@{domain_part}',
            mx_records,
            provider.__name__ if provider else None,
        )

    @staticmethod
    def _local_part_as_hostname(
        local_part: str,
        domain_part: str,
    ) -> tuple[str, str]:
        extracted = _tld_extract(domain_part)
        if extracted.subdomain:
            subdomain_parts = extracted.subdomain.split('.')
            local_part = subdomain_parts[0]
            remaining = (
                '.'.join(subdomain_parts[1:])
                if len(subdomain_parts) > 1
                else ''
            )
            components = []
            if remaining:
                components.append(remaining)
            if extracted.domain:
                components.append(extracted.domain)
            if extracted.suffix:
                components.append(extracted.suffix)
            domain_part = '.'.join(components)
        return local_part, domain_part

    @staticmethod
    def _lookup_provider_by_domain(
        domain_part: str,
    ) -> type[providers.MailboxProvider] | None:
        return providers.DomainMap.get(domain_part)

    @staticmethod
    def _lookup_provider(
        mx_records: list[tuple[int, str]],
    ) -> providers.MailboxProvider | None:
        for _priority, host in mx_records:
            lchost = host.lower()
            for provider in providers.Providers:
                for domain in provider.MXDomains:
                    if lchost.endswith(domain):
                        return provider
        return None

    def _skip_cache(self, domain: str) -> bool:
        if domain not in cache:
            return True
        elif cache[domain].expired:
            del cache[domain]
            return True
        return False


def normalize(
    email_address: str,
    skip_dns: bool = False,
) -> Result:
    """Normalize an email address.

    This function abstracts the asyncio base for this library and
    provides a blocking interface. If you intend to use this library
    as part of an asyncio-based application, use
    ``Normalizer.normalize`` instead.

    Args:
        email_address: The address to normalize.
        skip_dns: Skip DNS MX record lookups and use a static
            domain map to detect well-known mailbox providers.
            Defaults to ``False``.

    """

    async def _normalize():
        return await Normalizer(skip_dns=skip_dns).normalize(email_address)

    return asyncio.run(_normalize())
