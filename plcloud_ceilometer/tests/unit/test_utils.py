"""
# Author: Zhennan.luo(Jenner)
"""
__author__ = "Jenner.luo"

import mock
import unittest
from plcloud_ceilometer import utils


class TestUtils(unittest.TestCase):
    def setUp(self):
        pass

    def test_catch_log(self):
        mo = mock.Mock()

        @utils.catch_log
        def mock_func():
            raise Exception('Mock Exception!')
        mo.method_with_catch_log = mock_func

        mo.method_with_catch_log()
        mo.method_with_catch_log.assert_call()
        print (mo.method_with_catch_log)