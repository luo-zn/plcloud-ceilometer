"""
# Author: Zhennan.luo(Jenner)
"""
__author__ = "Jenner.luo"

import mock
from oslotest import base
from oslo_config import fixture as fixture_config
from ceilometer import service
from plcloud_ceilometer.clients.plcloudkitty import PLCloudkittyClient
from plcloudkittyclient import client as plck_client


class TestPLClient(base.BaseTestCase):
    def setUp(self):
        super(TestPLClient, self).setUp()
        conf = service.prepare_service([], [])
        self.CONF = self.useFixture(fixture_config.Config(conf)).conf
        self.useFixture(mockpatch.PatchObject(
            plck_client, '_get_endpoint',
            side_effect=self.plck_client_get_endpoint))
        self.plclient = PLCloudkittyClient(self.CONF)

    def plck_client_get_endpoint(self, *args, **kwargs):
        return "http://192.168.215.38:8899"

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
