"""
# Author: Zhennan.luo(Jenner)
"""
__author__ = "Jenner.luo"

import mock
from oslotest import base
from oslo_config import fixture as fixture_config, cfg
from plcloud_ceilometer.clients.cinder import CinderClient
from .. import fakes


class TestCinderClient(base.BaseTestCase):
    @mock.patch('ceilometer.keystone_client.get_session',
                fakes.keystone_client_get_session)
    def setUp(self):
        super(TestCinderClient, self).setUp()
        self.CONF = self.useFixture(fixture_config.Config()).conf
        self.register_service_credentials()
        self.cc = CinderClient(self.CONF)

    def register_service_credentials(self):
        group = "service_credentials"
        self.CONF.register_opts([cfg.StrOpt(
            'region_name', default="FakeRegion", help="Fake Region Name"),
            cfg.StrOpt('interface', default="public", choices=(
                'public', 'internal', 'admin', 'auth', 'publicURL',
                'internalURL', 'adminURL'), help="Fake interface"),
            cfg.BoolOpt('insecure', default=False, help="Fake insecure"),
        ], group=group)
        self.CONF.register_opts([cfg.StrOpt(
            'cinder', deprecated_name='cinderv2', default='volumev3',
            help='Cinder service type.'),
        ], group="service_types")

    def test_get_all_volume(self):
        print dir(self.cc)
