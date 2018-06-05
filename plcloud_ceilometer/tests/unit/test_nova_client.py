"""
# Author: Zhennan.luo(Jenner)
"""
__author__ = "Jenner.luo"

import mock
from oslotest import base
from oslo_config import fixture as fixture_config
from ceilometer import service
from plcloud_ceilometer.clients.nova import NovaClient


class TestNovaClient(base.BaseTestCase):
    def setUp(self):
        super(TestNovaClient, self).setUp()
        conf = service.prepare_service([], [])
        self.CONF = self.useFixture(fixture_config.Config(conf)).conf
        self.nvc = NovaClient(self.CONF)

    @classmethod
    def fake_servers_list(cls, *args, **kwargs):
        a = mock.MagicMock()
        a.id = 42
        a.name = "host-{}".format(b.id)
        a.user_id = '914947b388194de8ad1e9e2f7123bb78'
        a.addresses = {
            'demo-net': [{'OS-EXT-IPS-MAC:mac_addr': 'fa:16:3e:b8:b3:50',
                          'version': 4, 'addr': '10.0.0.9',
                          'OS-EXT-IPS:type': 'fixed'}]}
        a.flavor = {'id': 1}
        a.image = {'id': 1}
        b = mock.MagicMock()
        b.id = 43
        b.name = "host-{}".format(b.id)
        b.user_id = '914947b487184de8ad1e9e2f7123bb78'
        b.addresses = {'demo-net': [{'OS-EXT-IPS-MAC:mac_addr':
                                         'fa:15:4e:b8:b3:51',
                                     'version': 4, 'addr': '10.0.0.10',
                                     'OS-EXT-IPS:type': 'fixed'}]}
        b.flavor = {'id': 2}
        b.image = {'id': 2}
        return [a, b]

    @classmethod
    def fake_servers_get(cls, instance_id):
        return filter(lambda a: a.id == instance_id,
                      cls.fake_servers_list())[0]

    def test_get_all_instance(self):
        with mock.patch.object(self.nvc.client.servers, 'list',
                               side_effect=self.fake_servers_list):
            instances = self.nvc.get_all_instance()
        self.assertEqual(2, len(instances))
        self.assertEqual(42, instances[0].id)
        self.assertEqual(1, instances[0].flavor['id'])
        self.assertEqual(1, instances[0].image['id'])

    def test_get_instance(self):
        with mock.patch.object(self.nvc.client.servers, 'get',
                               side_effect=self.fake_servers_get):
            instance = self.nvc.get_instance(42)
            self.assertEqual(42, instance.id)
            self.assertEqual(1, instance.flavor['id'])
            self.assertEqual(1, instance.image['id'])
