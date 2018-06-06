"""
# Author: Zhennan.luo(Jenner)
"""
__author__ = "Jenner.luo"

import sys
import mock
import unittest
from plcloud_ceilometer import utils


class TestUtils(unittest.TestCase):
    def setUp(self):
        pass

    @classmethod
    def fake_sys_stdout(cls, *args, **kwargs):
        print args, kwargs

    def test_catch_log(self):
        with mock.path.object(sys, 'stdout', side_effect=self.fake_sys_stdout) as mo:
            print mo
            @utils.catch_log
            def mock_func():
                raise Exception('Mock Exception!')

            try:
                mock_func()
            except Exception as e:
                self.assertEqual(e.message, 'Mock Exception!')
