"""
# Author: Zhennan.luo(Jenner)
"""
__author__ = "Jenner.luo"

import mock
from oslotest import base
from .notifications import TestBase
from .. import fakes
from plcloud_ceilometer.billing.judger import Stop


class TestStop(TestBase):
    @property
    def message(self):
        return {u'_context_domain': None,
                u'_context_request_id': u'req-92bb634a-3637-4aef-ae0c-3e5f2d1736f8',
                u'_context_quota_class': None,
                u'event_type': u'plcloudkitty.billing.stop',
                u'_context_auth_token': u'004d7e1779074629a221d25da9c7d03b',
                u'_context_resource_uuid': None,
                u'payload': {u'state_description': u'',
                             u'availability_zone': u'nova',
                             u'terminated_at': u'',
                             u'res_type': u'instance', u'res_id': 1,
                             u'res_name': u'test-stop'
                             }}

    @mock.patch('plcloudkittyclient.client._get_endpoint',
                fakes.plck_client_get_endpoint)
    @mock.patch('ceilometer.keystone_client.get_session',
                fakes.keystone_client_get_session)
    def test_stop_instance(self):
        s = Stop(self.fake_manager)
        mock_stop = mock.patch.object(s.novaclient, 'stop')
        mock_stop.start()
        mock_log = fakes.getLogger()
        with mock.patch.object('oslo_log.log','getLogger',
                               return_value=mock_log):
            s.process_notification(self.message)
            mock_stop.get_original()[0].assert_called_once_with(
                self.message['payload']['res_id'])
            mock_log.info.assert_called()
        mock_stop.stop()
