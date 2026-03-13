"""Provider Specific Rules"""

import enum
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


class Apple(MailboxProvider):
    Flags = Rules.PLUS_ADDRESSING
    MXDomains = frozenset({'icloud.com'})


class Fastmail(MailboxProvider):
    Flags = Rules.PLUS_ADDRESSING ^ Rules.LOCAL_PART_AS_HOSTNAME
    MXDomains = frozenset({'messagingengine.com'})


class Google(MailboxProvider):
    Flags = Rules.PLUS_ADDRESSING ^ Rules.STRIP_PERIODS
    MXDomains = frozenset({'google.com', 'googlemail.com'})


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
