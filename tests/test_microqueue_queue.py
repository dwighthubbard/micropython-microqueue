#!/usr/bin/env python3
"""
Tests to validate microqueue is working properly with micropython
"""
# Notes:
#
# 1. These tests should be run with a cpython interpreter with the redislite module installed.
# 2. The micropython executable should be accesible in the path.
import logging
import hotqueue
import json
import redislite
import uredis_modular.list
from unittest import main, TestCase
import microqueue


class TestMicroqueue(TestCase):
    redis_test_port = 7800
    uredis_connection = None

    def setUp(self):
        self.redis_server = redislite.Redis(serverconfig={'port': self.redis_test_port})

    def tearDown(self):
        self.redis_server.shutdown()
        self.redis_server.shutdown()

    def test_init(self):
        queue = microqueue.MicroQueue('create', host='127.0.0.1', port=self.redis_test_port)

    def test_put(self):
        queue = microqueue.MicroQueue('put', host='127.0.0.1', port=self.redis_test_port)
        queue.put('test')
        self.assertIn(queue.key_name.encode(), self.redis_server.keys())
        self.assertEqual([b'"test"'], self.redis_server.lrange(queue.key_name, 0, -1))

    def test_get(self):
        queue = microqueue.MicroQueue('get', host='127.0.0.1', port=self.redis_test_port)
        self.redis_server.rpush(queue.key_name, '"test"')
        result = queue.get()
        self.assertEqual(result, "test")

    def test_clear(self):
        queue = microqueue.MicroQueue('clear', host='127.0.0.1', port=self.redis_test_port)
        self.redis_server.rpush(queue.key_name, '"test"')
        self.assertIn(queue.key_name.encode(), self.redis_server.keys())
        queue.clear()
        self.assertNotIn(queue.key_name.encode(), self.redis_server.keys())

    def test_get_hotqueue(self):
        queue = microqueue.MicroQueue('get', host='127.0.0.1', port=self.redis_test_port)
        queue2 = hotqueue.HotQueue('get', host='127.0.0.1', port=self.redis_test_port, serializer=json)
        queue2.put("test")
        result = queue.get()
        self.assertEqual(result, "test")


if __name__ == '__main__':
    logger = logging.getLogger('redislite')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    main()
