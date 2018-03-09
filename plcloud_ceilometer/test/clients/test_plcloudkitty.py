"""
# Author: Zhennan.luo(Jenner)
"""
__author__ = "Jenner.luo"

from oslotest import base
from oslo_config import fixture as fixture_config
from ceilometer import service


class TestPLClient(base.BaseTestCase):
    def setUp(self):
        super(TestPLClient, self).setUp()
        conf = service.prepare_service([], [])
        self.CONF = self.useFixture(fixture_config.Config(conf)).conf

    def test_conf_opts(self):
        print self.CONF
