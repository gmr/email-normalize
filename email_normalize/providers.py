"""
Provider Specific Rules
"""
import enum
import typing


class Rules(enum.Flag):
    """Represents what features a mailbox provider supports in dynamic
    aliasing of email addresses.

    Used to determine how to normalize provider specific email addresses.

    """
    DASH_ADDRESSING = enum.auto()
    PLUS_ADDRESSING = enum.auto()
    LOCAL_PART_AS_HOSTNAME = enum.auto()
    STRIP_PERIODS = enum.auto()


class MailboxProvider:
    """Base class to define the contract for the mail providers"""
    Flags: Rules
    MXDomains: typing.Set[str]


class Apple(MailboxProvider):
    Flags: Rules = Rules.PLUS_ADDRESSING
    MXDomains: typing.Set[str] = {'icloud.com'}


class Fastmail(MailboxProvider):
    Flags: Rules = Rules.PLUS_ADDRESSING ^ Rules.LOCAL_PART_AS_HOSTNAME
    MXDomains: typing.Set[str] = {'messagingengine.com'}


class Google(MailboxProvider):
    Flags: Rules = Rules.PLUS_ADDRESSING ^ Rules.STRIP_PERIODS
    MXDomains: typing.Set[str] = {'google.com'}


class Microsoft(MailboxProvider):
    Flags: Rules = Rules.PLUS_ADDRESSING
    MXDomains: typing.Set[str] = {'outlook.com'}


class ProtonMail(MailboxProvider):
    Flags: Rules = Rules.PLUS_ADDRESSING
    MXDomains: typing.Set[str] = {'protonmail.ch'}


class Rackspace(MailboxProvider):
    Flags: Rules = Rules.PLUS_ADDRESSING
    MXDomains: typing.Set[str] = {'emailsrvr.com'}


class Yahoo(MailboxProvider):
    Flags: Rules = Rules.DASH_ADDRESSING ^ Rules.STRIP_PERIODS
    MXDomains: typing.Set[str] = {'yahoodns.net'}


class Yandex(MailboxProvider):
    Flags: Rules = Rules.PLUS_ADDRESSING
    MXDomains: typing.Set[str] = {'mx.yandex.net', 'yandex.ru'}


class Zoho(MailboxProvider):
    Flags: Rules = Rules.PLUS_ADDRESSING
    MXDomains: typing.Set[str] = {'zoho.com'}


Providers = [
    Apple,
    Fastmail,
    Google,
    Microsoft,
    ProtonMail,
    Rackspace,
    Yahoo,
    Yandex,
    Zoho
]
