import asyncio
import unittest
import uuid
import warnings
from unittest import mock

import email_normalize


class TestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        warnings.simplefilter('ignore')


class InvalidDomainTestCase(TestCase):
    def test_invalid_domain_part(self):
        address = f'{uuid.uuid4()}@{uuid.uuid4()}'
        result = email_normalize.normalize(address)
        self.assertIsInstance(result, email_normalize.Result)
        self.assertEqual(result.address, address)
        self.assertEqual(result.normalized_address, address)
        self.assertListEqual(result.mx_records, [])
        self.assertIsNone(result.mailbox_provider)


class MailboxProviderTestCase(TestCase):
    def _perform_test(
        self,
        address: str,
        normalized: str,
        mx_records: list[tuple[int, str]],
        provider: str | None,
    ):
        with mock.patch(
            'email_normalize.Normalizer.mx_records',
        ) as mxr:
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
        address = f'{local_part}+test@{domain_part}'
        mx_records = [(10, 'mx01.mail.icloud.com')]
        self._perform_test(
            address, f'{local_part}@{domain_part}', mx_records, 'Apple'
        )

    def test_fastmail_plus_addressing(self):
        local_part = str(uuid.uuid4())
        domain_part = str(uuid.uuid4())
        address = f'{local_part}+test@{domain_part}'
        mx_records = [(10, 'in1-smtp.messagingengine.com')]
        self._perform_test(
            address, f'{local_part}@{domain_part}', mx_records, 'Fastmail'
        )

    def test_fastmail_local_part_as_hostname(self):
        local_part = str(uuid.uuid4())
        domain_part = f'{uuid.uuid4()}.com'
        address = f'testing@{local_part}.{domain_part}'
        mx_records = [(10, 'in1-smtp.messagingengine.com')]
        self._perform_test(
            address, f'{local_part}@{domain_part}', mx_records, 'Fastmail'
        )

    def test_fastmail_multi_segment_tld_no_subdomain(self):
        """Test domains with multi-segment TLDs but no subdomain."""
        local_part = str(uuid.uuid4())
        domain_part = f'{uuid.uuid4()}.co.uk'
        address = f'{local_part}@{domain_part}'
        mx_records = [(10, 'in1-smtp.messagingengine.com')]
        self._perform_test(
            address, f'{local_part}@{domain_part}', mx_records, 'Fastmail'
        )

    def test_fastmail_multi_segment_tld_with_subdomain(self):
        """Test domains with multi-segment TLDs and subdomains."""
        local_part = str(uuid.uuid4())
        domain_part = f'{uuid.uuid4()}.com.au'
        address = f'testing@{local_part}.{domain_part}'
        mx_records = [(10, 'in1-smtp.messagingengine.com')]
        self._perform_test(
            address, f'{local_part}@{domain_part}', mx_records, 'Fastmail'
        )

    def test_fastmail_complex_multi_segment_tld(self):
        """Test multiple subdomains with multi-segment TLD."""
        local_part = str(uuid.uuid4())
        subdomain_part = str(uuid.uuid4())
        domain_part = f'{uuid.uuid4()}.org.uk'
        address = f'testing@{local_part}.{subdomain_part}.{domain_part}'
        mx_records = [(10, 'in1-smtp.messagingengine.com')]
        self._perform_test(
            address,
            f'{local_part}@{subdomain_part}.{domain_part}',
            mx_records,
            'Fastmail',
        )

    def test_fastmail_deep_subdomain_single_tld(self):
        """Test deep subdomain structure with single TLD."""
        local_part = str(uuid.uuid4())
        subdomain1 = str(uuid.uuid4())
        subdomain2 = str(uuid.uuid4())
        domain_part = f'{uuid.uuid4()}.com'
        address = (
            f'testing@{local_part}.{subdomain1}.{subdomain2}.{domain_part}'
        )
        mx_records = [(10, 'in1-smtp.messagingengine.com')]
        self._perform_test(
            address,
            f'{local_part}@{subdomain1}.{subdomain2}.{domain_part}',
            mx_records,
            'Fastmail',
        )

    def test_google(self):
        local_part = str(uuid.uuid4()).replace('-', '.')
        domain_part = str(uuid.uuid4())
        address = f'{local_part}+test@{domain_part}'
        mx_records = [(1, 'aspmx.l.google.com')]
        self._perform_test(
            address,
            f'{local_part.replace(".", "")}@{domain_part}',
            mx_records,
            'Google',
        )

    def test_microsoft(self):
        local_part = str(uuid.uuid4())
        domain_part = str(uuid.uuid4())
        address = f'{local_part}+test@{domain_part}'
        mx_records = [(10, 'domain-com.mail.protection.outlook.com')]
        self._perform_test(
            address, f'{local_part}@{domain_part}', mx_records, 'Microsoft'
        )

    def test_protonmail(self):
        local_part = str(uuid.uuid4())
        domain_part = str(uuid.uuid4())
        address = f'{local_part}+test@{domain_part}'
        mx_records = [(5, 'mail.protonmail.ch')]
        self._perform_test(
            address, f'{local_part}@{domain_part}', mx_records, 'ProtonMail'
        )

    def test_rackspace(self):
        local_part = str(uuid.uuid4())
        domain_part = str(uuid.uuid4())
        address = f'{local_part}+test@{domain_part}'
        mx_records = [(10, 'mx1.emailsrvr.com')]
        self._perform_test(
            address, f'{local_part}@{domain_part}', mx_records, 'Rackspace'
        )

    def test_yahoo(self):
        local_part = str(uuid.uuid4())
        domain_part = str(uuid.uuid4())
        address = f'{local_part}@{domain_part}'
        mx_records = [(1, 'mta5.am0.yahoodns.net')]
        self._perform_test(
            address, f'{local_part}@{domain_part}', mx_records, 'Yahoo'
        )

    def test_yandex(self):
        local_part = str(uuid.uuid4())
        domain_part = str(uuid.uuid4())
        address = f'{local_part}+test@{domain_part}'
        mx_records = [(10, 'mx.yandex.net')]
        self._perform_test(
            address, f'{local_part}@{domain_part}', mx_records, 'Yandex'
        )

    def test_zoho(self):
        local_part = str(uuid.uuid4())
        domain_part = str(uuid.uuid4())
        address = f'{local_part}+test@{domain_part}'
        mx_records = [(10, 'mx.zoho.com')]
        self._perform_test(
            address, f'{local_part}@{domain_part}', mx_records, 'Zoho'
        )


class SkipDNSTestCase(TestCase):
    def _normalize(self, address):
        return email_normalize.normalize(address, skip_dns=True)

    def _assert_provider(self, domain, expected_provider):
        local_part = str(uuid.uuid4())
        address = f'{local_part}@{domain}'
        result = self._normalize(address)
        self.assertEqual(result.mailbox_provider, expected_provider)
        self.assertListEqual(result.mx_records, [])
        return result

    def test_gmail(self):
        self._assert_provider('gmail.com', 'Google')

    def test_googlemail(self):
        self._assert_provider('googlemail.com', 'Google')

    def test_outlook(self):
        self._assert_provider('outlook.com', 'Microsoft')

    def test_hotmail(self):
        self._assert_provider('hotmail.com', 'Microsoft')

    def test_live(self):
        self._assert_provider('live.com', 'Microsoft')

    def test_msn(self):
        self._assert_provider('msn.com', 'Microsoft')

    def test_icloud(self):
        self._assert_provider('icloud.com', 'Apple')

    def test_me(self):
        self._assert_provider('me.com', 'Apple')

    def test_mac(self):
        self._assert_provider('mac.com', 'Apple')

    def test_fastmail(self):
        self._assert_provider('fastmail.com', 'Fastmail')

    def test_fastmail_fm(self):
        self._assert_provider('fastmail.fm', 'Fastmail')

    def test_protonmail(self):
        self._assert_provider('protonmail.com', 'ProtonMail')

    def test_proton_me(self):
        self._assert_provider('proton.me', 'ProtonMail')

    def test_pm_me(self):
        self._assert_provider('pm.me', 'ProtonMail')

    def test_yahoo(self):
        self._assert_provider('yahoo.com', 'Yahoo')

    def test_yahoo_co_uk(self):
        self._assert_provider('yahoo.co.uk', 'Yahoo')

    def test_yahoo_co_jp(self):
        self._assert_provider('yahoo.co.jp', 'Yahoo')

    def test_ymail(self):
        self._assert_provider('ymail.com', 'Yahoo')

    def test_aol(self):
        self._assert_provider('aol.com', 'Yahoo')

    def test_yandex_com(self):
        self._assert_provider('yandex.com', 'Yandex')

    def test_yandex_ru(self):
        self._assert_provider('yandex.ru', 'Yandex')

    def test_ya_ru(self):
        self._assert_provider('ya.ru', 'Yandex')

    def test_zoho(self):
        self._assert_provider('zoho.com', 'Zoho')

    def test_zohomail(self):
        self._assert_provider('zohomail.com', 'Zoho')

    def test_google_rules_applied(self):
        result = self._normalize('u.s.e.r+tag@gmail.com')
        self.assertEqual(result.normalized_address, 'user@gmail.com')
        self.assertEqual(result.mailbox_provider, 'Google')

    def test_microsoft_plus_addressing(self):
        result = self._normalize('user+tag@outlook.com')
        self.assertEqual(result.normalized_address, 'user@outlook.com')

    def test_unknown_domain(self):
        domain = f'{uuid.uuid4()}.example.com'
        result = self._normalize(f'user@{domain}')
        self.assertIsNone(result.mailbox_provider)
        self.assertListEqual(result.mx_records, [])

    def test_dns_not_called(self):
        with mock.patch(
            'email_normalize.Normalizer.mx_records',
            side_effect=AssertionError('DNS should not be called'),
        ):
            result = self._normalize('test@gmail.com')
        self.assertEqual(result.mailbox_provider, 'Google')

    def test_async_normalizer(self):
        normalizer = email_normalize.Normalizer(skip_dns=True)
        result = asyncio.run(normalizer.normalize('u.s.e.r+tag@gmail.com'))
        self.assertEqual(result.normalized_address, 'user@gmail.com')
        self.assertEqual(result.mailbox_provider, 'Google')
        self.assertListEqual(result.mx_records, [])
