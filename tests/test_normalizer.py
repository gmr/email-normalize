import asyncio
import operator
import time
import unittest
import uuid
from unittest import mock

import aiodns

import email_normalize


class NormalizerTestCase(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.normalizer = email_normalize.Normalizer()
        email_normalize.cache.clear()

    def tearDown(self):
        email_normalize.cache.clear()

    async def test_mx_records(self):
        resolver = aiodns.DNSResolver()
        result = await resolver.query('gmail.com', 'MX')
        expectation = sorted(
            [(r.priority, r.host) for r in result],
            key=operator.itemgetter(0, 1))
        self.assertListEqual(
            await self.normalizer.mx_records('gmail.com'),
            expectation)

    async def test_cache(self):
        await self.normalizer.mx_records('gmail.com')
        await self.normalizer.mx_records('gmail.com')
        self.assertEqual(email_normalize.cache['gmail.com'].hits, 2)
        del email_normalize.cache['gmail.com']
        self.assertNotIn('gmail.com', email_normalize.cache)
        with self.assertRaises(KeyError):
            self.assertIsNone(email_normalize.cache['foo'])

    async def test_cache_max_size(self):
        for offset in range(0, self.normalizer.cache_limit):
            key = 'key-{}'.format(offset)
            email_normalize.cache[key] = email_normalize.CachedItem([], 60)
            email_normalize.cache[key].hits = 3
            email_normalize.cache[key].last_access = time.monotonic()

        key1 = 'gmail.com'
        await self.normalizer.mx_records(key1)

        self.assertNotIn('key-0', email_normalize.cache)

        key2 = 'github.com'
        await self.normalizer.mx_records(key2)
        self.assertNotIn(key1, email_normalize.cache)
        self.assertIn(key2, email_normalize.cache)

    async def test_cache_expiration(self):
        await self.normalizer.mx_records('gmail.com')
        cached_at = email_normalize.cache['gmail.com'].cached_at
        email_normalize.cache['gmail.com'].ttl = 1
        await asyncio.sleep(1)
        self.assertTrue(email_normalize.cache['gmail.com'].expired)
        await self.normalizer.mx_records('gmail.com')
        self.assertGreater(
            email_normalize.cache['gmail.com'].cached_at, cached_at)

    async def test_empty_mx_list(self):
        with mock.patch.object(self.normalizer, 'mx_records') as mx_records:
            mx_records.return_value = []
            result = await self.normalizer.normalize('foo@bar.com')
            self.assertEqual(result.normalized_address, 'foo@bar.com')
            self.assertIsNone(result.mailbox_provider)
            self.assertListEqual(result.mx_records, [])

    async def test_failure_cached(self):
        key = str(uuid.uuid4())
        records = await self.normalizer.mx_records(key)
        self.assertListEqual(records, [])
        self.assertIn(key, email_normalize.cache.keys())

    async def test_failure_not_cached(self):
        self.normalizer.cache_failures = False
        key = str(uuid.uuid4())
        records = await self.normalizer.mx_records(key)
        self.assertListEqual(records, [])

    async def test_weird_mx_list(self):
        with mock.patch.object(self.normalizer, 'mx_records') as recs:
            recs.return_value = [
                (1, str(uuid.uuid4())),
                (10, 'aspmx.l.google.com')
            ]
            result = await self.normalizer.normalize('f.o.o+bar@gmail.com')
            self.assertEqual(result.normalized_address, 'foo@gmail.com')
            self.assertEqual(result.mailbox_provider, 'Google')
