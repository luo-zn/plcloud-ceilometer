"""
# Author: Zhennan.luo(Jenner)
"""
__author__ = "Jenner.luo"

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
