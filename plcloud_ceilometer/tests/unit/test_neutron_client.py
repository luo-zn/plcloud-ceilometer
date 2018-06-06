"""
# Author: Zhennan.luo(Jenner)
"""
__author__ = "Jenner.luo"

import mock
from oslo_config import fixture as fixture_config, cfg
from oslotest import base
from plcloud_ceilometer.clients.neutron import NeutronClient
from . import fakes


class TestNeutronClient(base.BaseTestCase):
    @mock.patch('ceilometer.keystone_client.get_session',
                fakes.keystone_client_get_session)
    def setUp(self):
        super(TestNeutronClient, self).setUp()
        self.CONF = self.useFixture(fixture_config.Config()).conf
        self.register_service_credentials()
        self.nc = NeutronClient(self.CONF)
        self.nc.lb_version = 'v1'

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
            'neutron', default='FakeNetwork',
            help='Fake Neutron service type.'),
            cfg.StrOpt('neutron_lbaas_version', default='v2',
                       choices=('v1', 'v2'),
                       help='Neutron load balancer version.')
        ],
            group="service_types")

    @classmethod
    def fake_ports_list(cls, *args, **kwargs):
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

    @classmethod
    def fake_port(cls, *args, **kwargs):
        return {u'port': {u'allowed_address_pairs': [], u'extra_dhcp_opts': [],
                          u'updated_at': u'2018-05-30T09:57:34Z',
                          u'device_owner': u'network:router_interface_distributed',
                          u'revision_number': 6, u'binding:profile': {},
                          u'fixed_ips': [{
                              u'subnet_id': u'2350f8b6-3f23-4a95-a866-029487ae6875',
                              u'ip_address': u'10.0.0.1'}],
                          u'id': u'03b1a8bd-e26e-490d-9405-35e35103a86b',
                          u'security_groups': [], u'binding:vif_details': {},
                          u'binding:vif_type': u'distributed',
                          u'mac_address': u'fa:16:3e:d0:32:a7',
                          u'project_id': u'e354e01da1a54aab9b471b77422549e6',
                          u'status': u'ACTIVE', u'binding:host_id': u'',
                          u'description': u'', u'tags': [],
                          u'device_id': u'41a78164-329d-4230-9a89-f164f474044a',
                          u'name': u'demo-port', u'admin_state_up': True,
                          u'network_id': u'6d19bb1d-59cb-4bad-9bee-f73d6b1859e8',
                          u'tenant_id': u'e354e01da1a54aab9b471b77422549e6',
                          u'created_at': u'2018-05-30T09:57:26Z',
                          u'binding:vnic_type': u'normal'}}

    @classmethod
    def fake_routers_list(cls, *args, **kwargs):
        return {'routers': [{u'status': u'ACTIVE', u'external_gateway_info': {
            u'network_id': u'cab27061-a950-4d45-833d-81db34ce578e',
            u'enable_snat': True, u'external_fixed_ips': [
                {u'subnet_id': u'bd5bf8b8-2dbc-4d44-b03f-b01725a185b8',
                 u'ip_address': u'10.0.2.159'}]},
                             u'availability_zone_hints': [],
                             u'availability_zones': [u'nova'],
                             u'description': u'', u'tags': [],
                             u'tenant_id': u'e354e01da1a54aab9b471b77422549e6',
                             u'created_at': u'2018-05-30T09:57:24Z',
                             u'admin_state_up': True, u'distributed': True,
                             u'updated_at': u'2018-05-30T09:57:32Z',
                             u'ha': False, u'flavor_id': None,
                             u'revision_number': 10, u'routes': [],
                             u'project_id': u'e354e01da1a54aab9b471b77422549e6',
                             u'id': u'41a78164-329d-4230-9a89-f164f474044a',
                             u'name': u'demo-router'}]}

    @classmethod
    def fake_router(cls, *args, **kwargs):
        return {u'router': {u'status': u'ACTIVE', u'external_gateway_info': {
            u'network_id': u'cab27061-a950-4d45-833d-81db34ce578e',
            u'enable_snat': True, u'external_fixed_ips': [
                {u'subnet_id': u'bd5bf8b8-2dbc-4d44-b03f-b01725a185b8',
                 u'ip_address': u'10.0.2.159'}]},
                            u'availability_zone_hints': [],
                            u'availability_zones': [u'nova'],
                            u'description': u'', u'tags': [],
                            u'tenant_id': u'e354e01da1a54aab9b471b77422549e6',
                            u'created_at': u'2018-05-30T09:57:24Z',
                            u'admin_state_up': True, u'distributed': True,
                            u'updated_at': u'2018-05-30T09:57:32Z',
                            u'ha': False, u'flavor_id': None,
                            u'revision_number': 10, u'routes': [],
                            u'project_id': u'e354e01da1a54aab9b471b77422549e6',
                            u'id': u'41a78164-329d-4230-9a89-f164f474044a',
                            u'name': u'demo-router'}}

    def test_get_all_ports(self):
        with mock.patch.object(self.nc.client, 'list_ports',
                               side_effect=self.fake_ports_list):
            ports = self.nc.get_all_ports()
        self.assertEqual(1, len(ports))
        self.assertEqual('96d49cc3-4e01-40ce-9cac-c0e32642a442',
                         ports[0]['id'])

    def test_get_port(self):
        with mock.patch.object(self.nc.client, 'show_port',
                               side_effect=self.fake_port):
            port = self.nc.get_port('03b1a8bd-e26e-490d-9405-35e35103a86b')
            self.assertEqual('demo-port', port.get('name'))
            for key in ['name', 'id', 'project_id', 'tenant_id', 'status',
                        'mac_address', 'network_id','device_id']:
                self.assertIn(key, port)

    def test_get_router(self):
        with mock.patch.object(self.nc.client, 'show_router',
                               side_effect=self.fake_router):
            router = self.nc.get_router('41a78164-329d-4230-9a89-f164f474044a')
        self.assertEqual('demo-router', router.get('name'))
        for key in ['name', 'id', 'project_id', 'tenant_id', 'status',
                    'availability_zones', 'routes']:
            self.assertIn(key, router)

    def test_release_ip_call(self):
        with mock.patch.object(self.nc.client, 'delete_floatingip') as mo:
            self.nc.release_ip('aa-ee-aa')
            mo.assert_called_once_with('aa-ee-aa')
            print dir(mo)
