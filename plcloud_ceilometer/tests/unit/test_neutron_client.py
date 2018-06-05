"""
# Author: Zhennan.luo(Jenner)
"""
__author__ = "Jenner.luo"

import mock
from oslo_config import fixture as fixture_config
from oslotest import base
from plcloud_ceilometer.clients.neutron import NeutronClient
from . import fakes


class TestNeutronClient(base.BaseTestCase):
    @mock.patch('ceilometer.keystone_client.get_session',
                fakes.keystone_client_get_session)
    def setUp(self):
        super(TestNeutronClient, self).setUp()
        self.CONF = self.useFixture(fixture_config.Config()).conf
        self.nc = NeutronClient(self.CONF)
        self.nc.lb_version = 'v1'

    @staticmethod
    def fake_ports_list():
        return {'ports':
                [{'admin_state_up': True,
                  'device_id': '674e553b-8df9-4321-87d9-93ba05b93558',
                  'device_owner': 'network:router_gateway',
                  'extra_dhcp_opts': [],
                  'id': '96d49cc3-4e01-40ce-9cac-c0e32642a442',
                  'mac_address': 'fa:16:3e:c5:35:93',
                  'name': '',
                  'network_id': '298a3088-a446-4d5a-bad8-f92ecacd786b',
                  'status': 'ACTIVE',
                  'tenant_id': '89271fa581ab4380bf172f868c3615f9'},
                 ]}

    def test_get_all_ports(self):
        with mock.patch.object(self.nc.client, 'list_ports',
                               side_effect=self.fake_ports_list):
            ports = self.nc.get_all_ports()
        self.assertEqual(1, len(ports))
        self.assertEqual('96d49cc3-4e01-40ce-9cac-c0e32642a442',
                         ports[0]['id'])
