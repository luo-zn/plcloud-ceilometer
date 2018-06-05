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
    def fake_servers_list(cls,*args, **kwargs):
        a = mock.MagicMock()
        a.id = 42
        a.flavor = {'id': 1}
        a.image = {'id': 1}
        b = mock.MagicMock()
        b.id = 43
        b.flavor = {'id': 2}
        b.image = {'id': 2}
        return [a, b]

    def test_get_all_instance(self):
        with mock.patch.object(self.nvc.client.servers, 'list',
                               side_effect=self.fake_servers_list):
            instances = self.nvc.get_all_instance()
        self.assertEqual(2, len(instances))
        self.assertEqual(42, instances[0].id)
        self.assertEqual(1, instances[0].flavor['id'])
        self.assertEqual(1, instances[0].image['id'])