"""
# Author: Zhennan.luo(Jenner)
"""
__author__ = "Jenner.luo"

import mock
from oslotest import base
from oslo_config import fixture as fixture_config
from ceilometer import service
from plcloud_ceilometer.clients.plcloudkitty import PLCloudkittyClient


class TestPLClient(base.BaseTestCase):
    def setUp(self):
        super(TestPLClient, self).setUp()
        conf = service.prepare_service([], [])
        self.CONF = self.useFixture(fixture_config.Config(conf)).conf
        self.plclient = PLCloudkittyClient(self.CONF)

    @classmethod
    def fake_data_from_get_billing(cls):
        a = mock.MagicMock()
        a.res_type = 'compute.instance.end'
        a.res_meta = {'id': 666}
        a.region = 'RegionOne'
        a.billing_type = 1
        return a

    def test_get_billing(self):
        with mock.patch.object(
                self.plclient.client.billings.billing_manager,
                'get_billing', side_effect=self.fake_data_from_get_billing):
             billings = self.plclient.get_billing()
        for key in ['res_type', 'res_meta', 'region', 'billing_type']:
            self.assertIn(key, billings)
