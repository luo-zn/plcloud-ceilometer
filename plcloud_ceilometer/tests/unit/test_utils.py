"""
# Author: Zhennan.luo(Jenner)
"""
__author__ = "Jenner.luo"

import logging
import mock
import unittest
from plcloud_ceilometer import utils


class TestUtils(unittest.TestCase):
    def setUp(self):
        pass

    @classmethod
    def fake_getLogger(cls, *args, **kwargs):
        mock_logger = mock.Mock()
        mock_logger.exception = mock.Mock()
        return mock_logger

    def test_catch_log(self):
        with mock.patch('oslo_log.log.getLogger', self.fake_getLogger):
            @utils.catch_log
            def mock_func():
                raise Exception('Mock Exception!')

            try:
                mock_func()
            except Exception as e:
                self.assertEqual(e.message, 'Mock Exception!')
