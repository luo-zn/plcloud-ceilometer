"""
# Author: Zhennan.luo(Jenner)
"""
__author__ = "Jenner.luo"

from oslotest import base
from plcloud_ceilometer.billing.notifications import v1


class TestInstance(base.BaseTestCase):
    @property
    def message(self):
        return {u'_context_domain': None,
                u'_context_request_id': u'req-92bb634a-3637-4aef-ae0c-3e5f2d1736f8',
                u'_context_quota_class': None,
                'event_type': u'compute.instance.create.start',
                u'_context_auth_token': u'004d7e1779074629a221d25da9c7d03b',
                u'_context_resource_uuid': None,
                u'_context_user_id': u'914947b388194de8ad1e9e2f7123bb78',
                'payload': {u'state_description': u'',
                            u'availability_zone': u'nova',
                            u'terminated_at': u'',
                            u'ephemeral_gb': 0,
                            u'instance_type_id': 2,
                            u'deleted_at': u'',
                            u'reservation_id': u'r-vz96bc9m',
                            u'memory_mb': 2048,
                            u'display_name': u'qqqq',
                            u'hostname': u'qqqq',
                            u'state': u'building',
                            u'progress': u'',
                            u'launched_at': u'',
                            u'metadata': {}, u'node': None,
                            u'ramdisk_id': u'',
                            u'access_ip_v6': None,
                            u'disk_gb': 20,
                            u'access_ip_v4': None,
                            u'kernel_id': u'',
                            u'image_name': u'cirros',
                            u'host': None,
                            u'user_id': u'914947b388194de8ad1e9e2f7123bb78',
                            u'image_ref_url': u'http://10.0.1.16:9292/images/6942441f-09cc-40ab-a226-0f583b4e1bf8',
                            u'cell_name': u'', u'root_gb': 20,
                            u'tenant_id': u'e354e01da1a54aab9b471b77422549e6',
                            u'created_at': u'2018-05-30 10:04:30+00:00',
                            u'instance_id': u'2c466ea8-e25e-4e90-b713-418439765002',
                            u'instance_type': u'm1.small',
                            u'vcpus': 1,
                            u'image_meta': {
                                u'min_disk': u'20',
                                u'container_format': u'bare',
                                u'min_ram': u'0',
                                u'disk_format': u'qcow2',
                                u'base_image_ref': u'6942441f-09cc-40ab-a226-0f583b4e1bf8'},
                            u'architecture': None,
                            u'os_type': None,
                            u'instance_flavor_id': u'2'},
                u'_context_show_deleted': False,
                'priority': 'info',
                u'_context_is_admin': True,
                u'_context_project_domain': None,
                u'_context_timestamp': u'2018-05-30T10:04:27.538450',
                'publisher_id': u'compute.all-in-one',
                'message_id': u'4002408f-9993-4394-b44b-d4276a06f5b2',
                u'_context_roles': [u'admin'],
                'timestamp': u'2018-05-30 10:04:32.090320',
                u'_context_user': u'914947b388194de8ad1e9e2f7123bb78',
                u'_context_is_admin_project': True,
                u'_context_project_name': u'admin',
                u'_context_read_deleted': u'no',
                u'_context_user_identity': u'914947b388194de8ad1e9e2f7123bb78 e354e01da1a54aab9b471b77422549e6 - - -',
                u'_context_tenant': u'e354e01da1a54aab9b471b77422549e6',
                u'_context_instance_lock_checked': False,
                u'_context_project_id': u'e354e01da1a54aab9b471b77422549e6',
                u'_context_read_only': False,
                u'_context_user_domain': None,
                u'_context_user_name': u'admin',
                u'_context_remote_address': u'10.0.1.16'}

    def test_process_notification(self):
        sample_creation = v1.Instance(None)
        sample = sample_creation.process_notification(self.message)
        self.assertEqual(sample['user_id'], self.message['payload']['user_id'])
        self.assertEqual(sample['project_id'], self.message['payload']['tenant_id'])
        self.assertEqual(sample['res_id'], self.message['payload']['instance_id'])
        self.assertEqual(sample['res_name'], self.message['payload']['display_name'])
        self.assertEqual(sample['event_type'], self.message['event_type'])
        self.assertEqual(sample['timestamp'], self.message['timestamp'])
        self.assertEqual(sample['res_type'], 'instance')
        res_meta = {'memory_gb': self.message['payload']['memory_mb'] / 1024,
                    'vcpus': self.message['payload']['vcpus'],
                    'disk_gb': self.message['payload']['disk_gb'],
                    'ephemeral_gb': self.message['payload']['ephemeral_gb']}
        self.assertEqual(sample['res_meta'], res_meta)
