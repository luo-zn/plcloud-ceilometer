"""
# Author: Zhennan.luo(Jenner)
"""
__author__ = "Jenner.luo"

import mock
import unittest
from .. import fakes
from plcloud_ceilometer.utils import decorators


class TestUtils(unittest.TestCase):
    def test_catch_log(self):
        with mock.patch('oslo_log.log.getLogger', fakes.getLogger):
            @decorators.catch_log
            def mock_func():
                raise Exception('Mock Exception!')

            try:
                mock_func()
            except Exception as e:
                self.assertEqual(e.message, 'Mock Exception!')
