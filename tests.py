import unittest
import uuid

from email_normalize import _get_mx_exchanges, normalize


class InvalidDomainTests(unittest.TestCase):

    def test_invalid_domain_get_mx_exchanges(self):
        domain = '{0}.com'.format(uuid.uuid4().hex)
        self.assertEqual(_get_mx_exchanges(domain), [])


class FastMailTests(unittest.TestCase):

    def test_fastmail_variation_a(self):
        self.assertEqual(normalize('gavin.m.roy+123@fastmail.com'),
                         'gavin.m.roy@fastmail.com')

    def test_fastmail_variation_b(self):
        self.assertEqual(normalize('ignore-this+a@gavinmroy.fastmail.com'),
                         'gavinmroy@fastmail.com')


class GMailTests(unittest.TestCase):

    def test_gmail_domain_part(self):
        self.assertEqual(normalize('"Me!" <gavin.m.roy+123@gmail.com>'),
                         'gavinmroy@gmail.com')

    def test_mx_verification_normalization(self):
        self.assertEqual(normalize('gavin.r+123@aweber.net'),
                         'gavinr@aweber.net')


class MicrosoftTests(unittest.TestCase):

    def test_normalization(self):
        self.assertEqual(normalize('Gavin.M.Roy+123@Outlook.com'),
                         'gavin.m.roy@outlook.com')


class YahooTests(unittest.TestCase):

    def test_normalization(self):
        self.assertEqual(normalize('gavin.m.roy-folder-1@yahoo.com'),
                         'gavin.m.roy@yahoo.com')

    def test_normalization_tld_a(self):
        self.assertEqual(normalize('gavin.m.roy-folder-1@yahoo.co.in'),
                         'gavin.m.roy@yahoo.co.in')

    def test_normalization_tld_b(self):
        self.assertEqual(normalize('gavin.m.roy-folder-1@yahoo.at'),
                         'gavin.m.roy@yahoo.at')


class NormalDomainTests(unittest.TestCase):

    def test_normalization(self):
        self.assertEqual(normalize('gavin.m.roy+123@godaddy.com'),
                         'gavin.m.roy+123@godaddy.com')
