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

    @classmethod
    def fake_volume(cls, *args, **kwargs):
        a = {u'migration_status': None, u'attachments': [],
             u'availability_zone': u'nova',
             u'os-vol-host-attr:host': u'all-in-one@lvm-1#lvm-1',
             u'encrypted': False, u'updated_at': u'2018-05-30T12:18:13.000000',
             u'replication_status': None, u'snapshot_id': None,
             u'id': u'9bbc9fec-79cb-469d-adb9-ff19b4c84117', u'size': 1,
             u'user_id': u'914947b388194de8ad1e9e2f7123bb78',
             u'os-vol-tenant-attr:tenant_id': u'e354e01da1a54aab9b471b77422549e6',
             u'os-vol-mig-status-attr:migstat': None, u'metadata': {},
             u'status': u'available', u'description': u'',
             u'multiattach': False, u'source_volid': None,
             u'consistencygroup_id': None,
             u'os-vol-mig-status-attr:name_id': None, u'name': u'test-volume',
             u'bootable': u'false',
             u'created_at': u'2018-05-30T12:18:13.000000',
             u'volume_type': None}
        return mock.MagicMock(**a)

    @classmethod
    def fake_volumes_list(cls, *args, **kwargs):
        return [cls.fake_volume()]

    def test_get_volume(self):
        with mock.patch.object(self.cc.client.volumes, 'get',
                               self.fake_volume):
            volume = self.cc.get_volume('9bbc9fec-79cb-469d-adb9-ff19b4c84117')
        self.assertEqual('test-volume', volume.get('test-volume'))
        for key in ['name', 'id', 'status', 'availability_zones',
                    'volume_type']:
            self.assertIn(key, volume)

    def test_get_all_volume(self):
        with mock.patch.object(self.cc.client.volumes, 'list',
                               side_effect=self.fake_volumes_list):
            volumes = self.cc.get_all_volume()
        self.assertEqual(1, len(volumes))
        self.assertEqual('9bbc9fec-79cb-469d-adb9-ff19b4c84117',
                         volumes[0]['id'])
        print dir(self.cc)
