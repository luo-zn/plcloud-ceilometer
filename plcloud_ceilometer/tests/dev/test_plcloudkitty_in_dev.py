"""
# Author: Zhennan.luo(Jenner)
"""
__author__ = "Jenner.luo"

import unittest
from oslotest import base
from oslo_config import fixture as fixture_config
from ceilometer import service
from plcloud_ceilometer.clients.plcloudkitty import PLCloudkittyClient


class TestPLClient(base.BaseTestCase):
    def setUp(self):
        super(TestPLClient, self).setUp()
        conf = service.prepare_service()
        self.plclient = PLCloudkittyClient(conf)

    def test_plcloudkitty_client(self):
        print self.plclient


if __name__ == '__main__':
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    test_cases = [
        {'case': TestPLClient, "methods": ["test_plcloudkitty_client",]},
    ]
    for item in test_cases:
        methods = item.get('methods', [])
        case = item.get('case')
        if methods:
            for method_name in methods:
                suite.addTest(case(method_name))
        else:
            tests = loader.loadTestsFromTestCase(case)
            suite.addTests(tests)
    unittest.TextTestRunner(verbosity=2).run(suite)