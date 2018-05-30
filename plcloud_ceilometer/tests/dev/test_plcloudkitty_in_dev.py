"""
# Author: Zhennan.luo(Jenner)
"""
__author__ = "Jenner.luo"

import unittest
from oslotest import base
from oslo_config import fixture as fixture_config
from ceilometer import service
from plcloud_ceilometer.clients.plcloudkitty import PLCloudkittyClient
from plcloudkittyclient.common import utils


class TestPLClient(unittest.TestCase):
    def setUp(self):
        super(TestPLClient, self).setUp()
        conf = service.prepare_service()
        self.plclient = PLCloudkittyClient(conf)

    @classmethod
    def get_plcloudkitty_client(cls, version):
        module = utils.import_versioned_module(version, 'client')
        return getattr(module, 'Client')

    def test_plcloudkitty_client(self):
        self.assertIsInstance(self.plclient, PLCloudkittyClient)
        plcloudkitty_client = self.get_plcloudkitty_client('1')
        self.assertIsInstance(self.plclient.client, plcloudkitty_client)


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
