"""Provider Specific Rules"""

import collections.abc
import enum
import types
import typing


class Rules(enum.Flag):
    """Represents what features a mailbox provider supports in dynamic
    aliasing of email addresses.

    Used to determine how to normalize provider specific email addresses.

    """

    NONE = 0
    PLUS_ADDRESSING = enum.auto()
    LOCAL_PART_AS_HOSTNAME = enum.auto()
    STRIP_PERIODS = enum.auto()


class MailboxProvider:
    """Base class to define the contract for the mail providers."""

    Flags: typing.ClassVar[Rules]
    MXDomains: typing.ClassVar[frozenset[str]]

    # Domains for which ``Rules.STRIP_PERIODS`` should be applied. Period
    # stripping is only correct for a provider's consumer domains, not for
    # custom domains that happen to route mail through the same MX servers
    # (e.g. Google Workspace). An empty set means period stripping applies
    # to every domain matched to the provider.
    StripPeriodDomains: typing.ClassVar[frozenset[str]] = frozenset()

    # Map of alias domains to the provider's canonical domain. Alias
    # domains deliver to the same mailbox as their canonical target
    # (e.g. Apple's me.com/mac.com and icloud.com), so the domain part is
    # folded to the canonical form during normalization. This is only
    # correct for a provider's own consumer alias domains, never for
    # custom domains that merely share the same MX servers. An empty
    # mapping means no domain folding is performed.
    CanonicalDomains: typing.ClassVar[collections.abc.Mapping[str, str]] = (
        types.MappingProxyType({})
    )


class Apple(MailboxProvider):
    Flags = Rules.PLUS_ADDRESSING
    MXDomains = frozenset({'icloud.com'})
    # me.com and mac.com are legacy alias domains for the same iCloud
    # mailbox. See https://support.apple.com/en-us/118230.
    CanonicalDomains = types.MappingProxyType(
        {'me.com': 'icloud.com', 'mac.com': 'icloud.com'}
    )


class Fastmail(MailboxProvider):
    Flags = Rules.PLUS_ADDRESSING | Rules.LOCAL_PART_AS_HOSTNAME
    MXDomains = frozenset({'messagingengine.com'})


class Google(MailboxProvider):
    Flags = Rules.PLUS_ADDRESSING | Rules.STRIP_PERIODS
    MXDomains = frozenset({'google.com', 'googlemail.com'})
    # Only consumer Gmail strips dots; Google Workspace custom domains do
    # not. See https://support.google.com/mail/answer/7436150.
    StripPeriodDomains = frozenset({'gmail.com', 'googlemail.com'})
    # googlemail.com is an alias domain for consumer Gmail; it delivers to
    # the same mailbox as gmail.com. See
    # https://support.google.com/mail/answer/10313.
    CanonicalDomains = types.MappingProxyType({'googlemail.com': 'gmail.com'})


class Microsoft(MailboxProvider):
    Flags = Rules.PLUS_ADDRESSING
    MXDomains = frozenset({'outlook.com'})


class ProtonMail(MailboxProvider):
    Flags = Rules.PLUS_ADDRESSING
    MXDomains = frozenset({'protonmail.ch'})


class Rackspace(MailboxProvider):
    Flags = Rules.PLUS_ADDRESSING
    MXDomains = frozenset({'emailsrvr.com'})


class Yahoo(MailboxProvider):
    # No normalization rules — Yahoo disposable addresses use the format
    # nickname-keyword@, where the nickname alone is not a deliverable
    # address. See https://help.yahoo.com/kb/SLN28815.html
    Flags = Rules.NONE
    MXDomains = frozenset({'yahoodns.net'})


class Yandex(MailboxProvider):
    Flags = Rules.PLUS_ADDRESSING
    MXDomains = frozenset({'mx.yandex.net', 'yandex.ru'})


class Zoho(MailboxProvider):
    Flags = Rules.PLUS_ADDRESSING
    MXDomains = frozenset({'zoho.com'})


Providers = [
    Apple,
    Fastmail,
    Google,
    Microsoft,
    ProtonMail,
    Rackspace,
    Yahoo,
    Yandex,
    Zoho,
]

DomainMap: dict[str, type[MailboxProvider]] = {
    'icloud.com': Apple,
    'me.com': Apple,
    'mac.com': Apple,
    'fastmail.com': Fastmail,
    'fastmail.fm': Fastmail,
    'gmail.com': Google,
    'googlemail.com': Google,
    'outlook.com': Microsoft,
    'hotmail.com': Microsoft,
    'live.com': Microsoft,
    'msn.com': Microsoft,
    'proton.me': ProtonMail,
    'protonmail.com': ProtonMail,
    'pm.me': ProtonMail,
    'yahoo.com': Yahoo,
    'yahoo.co.uk': Yahoo,
    'yahoo.co.jp': Yahoo,
    'ymail.com': Yahoo,
    'aol.com': Yahoo,
    'yandex.com': Yandex,
    'yandex.ru': Yandex,
    'ya.ru': Yandex,
    'zoho.com': Zoho,
    'zohomail.com': Zoho,
}
