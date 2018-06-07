"""
# Author: Zhennan.luo(Jenner)
"""
__author__ = "Jenner.luo"

import mock
from oslotest import base
from oslo_config import fixture as fixture_config, cfg
from plcloud_ceilometer.clients.cinder import CinderClient
from .. import fakes

a = {u'migration_status': None, u'attachments': [],
     u'availability_zone': u'nova',
     u'os-vol-host-attr:host': u'all-in-one@lvm-1#lvm-1'}


class FakeObject(object):
    def __init__(self, dict_):
        for key, val in dict_.iteritems():
            setattr(self, key, val)


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
             u'status': u'in-use', u'description': u'',
             u'multiattach': False, u'source_volid': None,
             u'consistencygroup_id': None,
             u'os-vol-mig-status-attr:name_id': None, u'name': u'test-volume',
             u'bootable': u'false',
             u'created_at': u'2018-05-30T12:18:13.000000',
             u'volume_type': None}
        m = mock.MagicMock(**a)
        m.attrs = a.keys()
        m.detach = mock.MagicMock()
        m.delete = mock.MagicMock()
        return m

    @classmethod
    def fake_volumes_list(cls, *args, **kwargs):
        return [cls.fake_volume()]

    @classmethod
    def fake_snapshot(cls, *args, **kwargs):
        a = {u'status': u'available',
             u'os-extended-snapshot-attributes:progress': u'100%',
             u'description': u'',
             u'os-extended-snapshot-attributes:project_id': u'e354e01da1a54aab9b471b77422549e6',
             u'size': 1, u'updated_at': u'2018-06-06T11:15:45.000000',
             u'id': u'e6bd5b76-84fb-4cf2-9f3d-9b625c031804',
             u'volume_id': u'9bbc9fec-79cb-469d-adb9-ff19b4c84117',
             u'metadata': {}, u'created_at': u'2018-06-06T11:15:42.000000',
             u'name': u'snapshot1'}
        m = mock.MagicMock(**a)
        m.delete = mock.MagicMock()
        return a

    @classmethod
    def fake_snapshot_list(cls, *args, **kwargs):
        return [cls.fake_snapshot()]

    def test_get_volume(self):
        with mock.patch.object(self.cc.client.volumes, 'get',
                               self.fake_volume):
            volume = self.cc.get_volume('9bbc9fec-79cb-469d-adb9-ff19b4c84117')
        for key in ['id', 'status', 'availability_zone', 'volume_type']:
            self.assertIn(key, volume.attrs)

    def test_get_all_volume(self):
        with mock.patch.object(self.cc.client.volumes, 'list',
                               side_effect=self.fake_volumes_list):
            volumes = self.cc.get_all_volume()
        self.assertEqual(1, len(volumes))
        self.assertEqual('9bbc9fec-79cb-469d-adb9-ff19b4c84117',
                         volumes[0].id)

    @mock.patch('plcloud_ceilometer.clients.cinder.CinderClient.client'
                '.volume_snapshots.delete', lambda x: x)
    def test_delete_volume(self, mock_delete):
        with mock.patch.object(self.cc.client.volumes, 'get',
                               side_effect=self.fake_volume):
            with mock.patch.object(self.cc.client.volume_snapshots, 'list',
                                   side_effect=self.fake_snapshot_list):
                volume = self.cc.delete_volume(
                    '9bbc9fec-79cb-469d-adb9-ff19b4c84117')
                volume.detach.assert_called_once_with()
                volume.delete.assert_called_once_with()
                mock_delete.assert_called_once_with()
