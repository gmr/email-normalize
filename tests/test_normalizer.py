import asyncio
import functools
import logging
import operator
import os
import time
import unittest
import uuid

import aiodns
from asynctest import mock

import email_normalize

LOGGER = logging.getLogger(__name__)


def async_test(*func):
    if func:
        @functools.wraps(func[0])
        def wrapper(*args, **kwargs):
            LOGGER.debug('Starting test with loop %r', args[0])
            args[0].loop.run_until_complete(func[0](*args, **kwargs))
            LOGGER.debug('Test completed')
        return wrapper


class AsyncTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.set_debug(True)
        self.timeout = int(os.environ.get('ASYNC_TIMEOUT', '5'))
        self.timeout_handle = self.loop.call_later(
            self.timeout, self.on_timeout)
        self.resolver = aiodns.DNSResolver(loop=self.loop)
        self.normalizer = email_normalize.Normalizer()
        self.normalizer._resolver = self.resolver
        email_normalize.cache = {}

    def tearDown(self):
        LOGGER.debug('In AsyncTestCase.tearDown')
        if not self.timeout_handle.cancelled():
            self.timeout_handle.cancel()
        self.loop.run_until_complete(self.loop.shutdown_asyncgens())
        if self.loop.is_running:
            self.loop.close()
        super().tearDown()

    def on_timeout(self):
        self.loop.stop()
        raise TimeoutError(
            'Test duration exceeded {} seconds'.format(self.timeout))


class NormalizerTestCase(AsyncTestCase):

    def setUp(self) -> None:
        super().setUp()
        if 'gmail.com' in email_normalize.cache:
            del email_normalize.cache['gmail.com']

    @async_test
    async def test_mx_records(self):
        result = await self.resolver.query('gmail.com', 'MX')
        expectation = []
        for record in result:
            expectation.append((record.priority, record.host))
        expectation.sort(key=operator.itemgetter(0, 1))
        self.assertListEqual(
            await self.normalizer.mx_records('gmail.com'),
            expectation)

    @async_test
    async def test_cache(self):
        await self.normalizer.mx_records('gmail.com')
        await self.normalizer.mx_records('gmail.com')
        self.assertEqual(email_normalize.cache['gmail.com'].hits, 2)
        del email_normalize.cache['gmail.com']
        self.assertNotIn('gmail.com', email_normalize.cache)
        with self.assertRaises(KeyError):
            self.assertIsNone(email_normalize.cache['foo'])

    @async_test
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

    @async_test
    async def test_cache_expiration(self):
        await self.normalizer.mx_records('gmail.com')
        cached_at = email_normalize.cache['gmail.com'].cached_at
        email_normalize.cache['gmail.com'].ttl = 1
        await asyncio.sleep(1)
        self.assertTrue(email_normalize.cache['gmail.com'].expired)
        await self.normalizer.mx_records('gmail.com')
        self.assertGreater(
            email_normalize.cache['gmail.com'].cached_at, cached_at)

    @async_test
    async def test_empty_mx_list(self):
        with mock.patch.object(self.normalizer, 'mx_records') as mx_records:
            mx_records.return_value = []
            result = await self.normalizer.normalize('foo@bar.com')
            self.assertEqual(result.normalized_address, 'foo@bar.com')
            self.assertIsNone(result.mailbox_provider)
            self.assertListEqual(result.mx_records, [])

    @async_test
    async def test_failure_cached(self):
        key = str(uuid.uuid4())
        records = await self.normalizer.mx_records(key)
        self.assertListEqual(records, [])
        self.assertIn(key, email_normalize.cache.keys())

    @async_test
    async def test_failure_not_cached(self):
        email_normalize.cache_failures = False
        key = str(uuid.uuid4())
        records = await self.normalizer.mx_records(key)
        self.assertListEqual(records, [])
        email_normalize.cache_failures = True

    @async_test
    async def test_weird_mx_list(self):
        with mock.patch.object(self.normalizer, 'mx_records') as recs:
            recs.return_value = [
                (1, str(uuid.uuid4())),
                (10, 'aspmx.l.google.com')
            ]
            result = await self.normalizer.normalize('f.o.o+bar@gmail.com')
            self.assertEqual(result.normalized_address, 'foo@gmail.com')
            self.assertEqual(result.mailbox_provider, 'Google')
