"""
# Author: Zhennan.luo(Jenner)
"""
__author__ = "Jenner.luo"

import mock
from oslotest import base
from .notifications import TestBase
from plcloud_ceilometer.billing.judger import Stop


class TestStop(TestBase):
    @property
    def message(self):
        return {u'_context_domain': None,
                u'_context_request_id': u'req-92bb634a-3637-4aef-ae0c-3e5f2d1736f8',
                u'_context_quota_class': None,
                'event_type': u'plcloudkitty.billing.stop',
                u'_context_auth_token': u'004d7e1779074629a221d25da9c7d03b',
                u'_context_resource_uuid': None,
                'payload': {u'state_description': u'',
                            u'availability_zone': u'nova',
                            u'terminated_at': u'',
                            'res_type': 'instance', 'res_id': 1,
                            'res_name':'test-stop'
                            }}

    def test_stop_instance(self):
        s = Stop(self.fake_manager)
        ns = mock.pach.object(s.novaclient, 'stop')
        ns.start()
        s.process_notification(self.message)
        mock_delete.get_original()[0].assert_called_once_with(
            self.message['payload']['res_id'])
        ns.stop()
