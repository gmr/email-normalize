import typing
import unittest
import uuid
import warnings

from asynctest import mock

import email_normalize


class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        warnings.simplefilter('ignore')


class InvalidDomainTestCase(TestCase):

    def test_invalid_domain_part(self):
        address = '{}@{}'.format(uuid.uuid4(), uuid.uuid4())
        result = email_normalize.normalize(address)
        self.assertIsInstance(result, email_normalize.Result)
        self.assertEqual(result.address, address)
        self.assertEqual(result.normalized_address, address)
        self.assertListEqual(result.mx_records, [])
        self.assertIsNone(result.mailbox_provider)


class MailboxProviderTestCase(TestCase):

    def _perform_test(self,
                      address: str,
                      normalized: str,
                      mx_records: typing.List[typing.Tuple[int, str]],
                      provider: typing.Optional[str]):
        with mock.patch('email_normalize.Normalizer.mx_records') as mxr:
            mxr.return_value = mx_records
            result = email_normalize.normalize(address)
        self.assertIsInstance(result, email_normalize.Result)
        self.assertEqual(result.address, address)
        self.assertEqual(result.normalized_address, normalized)
        self.assertListEqual(result.mx_records, mx_records)
        self.assertEqual(result.mailbox_provider, provider)

    def test_apple(self):
        local_part = str(uuid.uuid4())
        domain_part = str(uuid.uuid4())
        address = '{}+test@{}'.format(local_part, domain_part)
        mx_records = [(10, 'mx01.mail.icloud.com')]
        self._perform_test(
            address, '{}@{}'.format(local_part, domain_part),
            mx_records, 'Apple')

    def test_fastmail_plus_addressing(self):
        local_part = str(uuid.uuid4())
        domain_part = str(uuid.uuid4())
        address = '{}+test@{}'.format(local_part, domain_part)
        mx_records = [(10, 'in1-smtp.messagingengine.com')]
        self._perform_test(
            address, '{}@{}'.format(local_part, domain_part),
            mx_records, 'Fastmail')

    def test_fastmail_local_part_as_hostname(self):
        local_part = str(uuid.uuid4())
        domain_part = '{}.com'.format(uuid.uuid4())
        address = 'testing@{}.{}'.format(local_part, domain_part)
        mx_records = [(10, 'in1-smtp.messagingengine.com')]
        self._perform_test(
            address, '{}@{}'.format(local_part, domain_part),
            mx_records, 'Fastmail')

    def test_fastmail_multi_segment_tld_no_subdomain(self):
        """Test that domains with multi-segment TLDs but no subdomain are not modified."""
        local_part = str(uuid.uuid4())
        domain_part = '{}.co.uk'.format(uuid.uuid4())
        address = '{}@{}'.format(local_part, domain_part)
        mx_records = [(10, 'in1-smtp.messagingengine.com')]
        self._perform_test(
            address, '{}@{}'.format(local_part, domain_part),
            mx_records, 'Fastmail')

    def test_fastmail_multi_segment_tld_with_subdomain(self):
        """Test that domains with multi-segment TLDs and subdomains are correctly normalized."""
        local_part = str(uuid.uuid4())
        domain_part = '{}.com.au'.format(uuid.uuid4())
        address = 'testing@{}.{}'.format(local_part, domain_part)
        mx_records = [(10, 'in1-smtp.messagingengine.com')]
        self._perform_test(
            address, '{}@{}'.format(local_part, domain_part),
            mx_records, 'Fastmail')

    def test_fastmail_complex_multi_segment_tld(self):
        """Test complex case with multiple subdomains and multi-segment TLD."""
        local_part = str(uuid.uuid4())
        subdomain_part = str(uuid.uuid4())
        domain_part = '{}.org.uk'.format(uuid.uuid4())
        address = 'testing@{}.{}.{}'.format(local_part, subdomain_part, domain_part)
        mx_records = [(10, 'in1-smtp.messagingengine.com')]
        self._perform_test(
            address, '{}@{}.{}'.format(local_part, subdomain_part, domain_part),
            mx_records, 'Fastmail')

    def test_fastmail_deep_subdomain_single_tld(self):
        """Test deep subdomain structure with single TLD."""
        local_part = str(uuid.uuid4())
        subdomain1 = str(uuid.uuid4())
        subdomain2 = str(uuid.uuid4())
        domain_part = '{}.com'.format(uuid.uuid4())
        address = 'testing@{}.{}.{}.{}'.format(local_part, subdomain1, subdomain2, domain_part)
        mx_records = [(10, 'in1-smtp.messagingengine.com')]
        self._perform_test(
            address, '{}@{}.{}.{}'.format(local_part, subdomain1, subdomain2, domain_part),
            mx_records, 'Fastmail')

    def test_google(self):
        local_part = str(uuid.uuid4()).replace('-', '.')
        domain_part = str(uuid.uuid4())
        address = '{}+test@{}'.format(local_part, domain_part)
        mx_records = [(1, 'aspmx.l.google.com')]
        self._perform_test(
            address, '{}@{}'.format(local_part.replace('.', ''), domain_part),
            mx_records, 'Google')

    def test_microsoft(self):
        local_part = str(uuid.uuid4())
        domain_part = str(uuid.uuid4())
        address = '{}+test@{}'.format(local_part, domain_part)
        mx_records = [(10, 'domain-com.mail.protection.outlook.com')]
        self._perform_test(
            address, '{}@{}'.format(local_part, domain_part),
            mx_records, 'Microsoft')

    def test_protonmail(self):
        local_part = str(uuid.uuid4())
        domain_part = str(uuid.uuid4())
        address = '{}+test@{}'.format(local_part, domain_part)
        mx_records = [(5, 'mail.protonmail.ch')]
        self._perform_test(
            address, '{}@{}'.format(local_part, domain_part),
            mx_records, 'ProtonMail')

    def test_rackspace(self):
        local_part = str(uuid.uuid4())
        domain_part = str(uuid.uuid4())
        address = '{}+test@{}'.format(local_part, domain_part)
        mx_records = [(10, 'mx1.emailsrvr.com')]
        self._perform_test(
            address, '{}@{}'.format(local_part, domain_part),
            mx_records, 'Rackspace')

    def test_yahoo(self):
        local_part = str(uuid.uuid4())
        domain_part = str(uuid.uuid4())
        address = '{}@{}'.format(local_part, domain_part)
        mx_records = [(1, 'mta5.am0.yahoodns.net')]
        self._perform_test(
            address, '{}@{}'.format(local_part.split('-', 1)[0], domain_part),
            mx_records, 'Yahoo')

    def test_yandex(self):
        local_part = str(uuid.uuid4())
        domain_part = str(uuid.uuid4())
        address = '{}+test@{}'.format(local_part, domain_part)
        mx_records = [(10, 'mx.yandex.net')]
        self._perform_test(
            address, '{}@{}'.format(local_part, domain_part),
            mx_records, 'Yandex')

    def test_zoho(self):
        local_part = str(uuid.uuid4())
        domain_part = str(uuid.uuid4())
        address = '{}+test@{}'.format(local_part, domain_part)
        mx_records = [(10, 'mx.zoho.com')]
        self._perform_test(
            address, '{}@{}'.format(local_part, domain_part),
            mx_records, 'Zoho')
