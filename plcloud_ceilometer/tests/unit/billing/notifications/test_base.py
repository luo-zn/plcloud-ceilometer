"""
# Author: Zhennan.luo(Jenner)
"""
__author__ = "Jenner.luo"

import mock
from oslotest import base
from oslo_config import fixture as fixture_config, cfg
from plcloud_ceilometer.billing.notifications import base as plugin_base
from plcloud_ceilometer.tests.unit import fakes


class TestBillingBase(base.BaseTestCase):
    def setUp(self):
        super(TestBillingBase, self).setUp()
        self.CONF = self.useFixture(fixture_config.Config()).conf
        self.register_service_credentials()

    class FakeBillingBase(plugin_base.BillingBase):
        event_types = ['compute.*']

        def process_notification(self, message):
            pass

        def plcloudkitty_billing(self, notification):
            pass

    def register_service_credentials(self):
        group = "service_credentials"
        self.CONF.register_opts([cfg.StrOpt(
            'region_name', default="FakeRegion", help="Fake Region Name"),
            cfg.BoolOpt('insecure', default=False, help="Fake insecure"),
        ], group=group)

    @property
    def fake_manager(self):
        manager = mock.Mock()
        manager.conf = self.CONF
        return manager

    @property
    def fake_message(self):
        return {
            'ctxt': {'user_id': 'fake_user_id',
                     'project_id': 'fake_project_id'},
            'publisher_id': 'fake.publisher_id',
            'event_type': 'fake.event',
            'payload': {'foo': 'bar'},
            'metadata': {'message_id': '3577a84f-29ec-4904-9566-12c52289c2e8',
                         'timestamp': '2015-06-1909:19:35.786893'}
        }

    @property
    def fake_notification(self):
        return {
            'priority': 'info',
            'event_type': 'fake.event',
            'timestamp': '2015-06-1909:19:35.786893',
            '_context_user_id': 'fake_user_id',
            '_context_project_id': 'fake_project_id',
            'publisher_id': 'fake.publisher_id',
            'payload': {'foo': 'bar'},
            'message_id': '3577a84f-29ec-4904-9566-12c52289c2e8'
        }

    @mock.patch('plcloudkittyclient.client._get_endpoint',
                fakes.plck_client_get_endpoint)
    @mock.patch('ceilometer.keystone_client.get_session',
                fakes.keystone_client_get_session)
    def test_plcloudkitty_billing(self):
        plugin = self.FakeBillingBase(self.fake_manager)
        # plugin.to_samples_and_publish = mock.Mock()
        plugin._process_notifications = mock.Mock()
        plugin.plcloudkitty_billing = mock.Mock()
        plugin.need_to_handle = mock.Mock()
        plugin.process_notification = mock.Mock()
        plugin._create_billing = mock.Mock()

        plugin.info([self.fake_message])

        plugin._process_notifications.assert_called_once_with(
            'info', [self.fake_notification])
        #plugin.plcloudkitty_billing.assert_called_with(self.fake_notification)
        plugin.plcloudkitty_billing.assert_called_once_with(self.fake_notification)
        plugin.need_to_handle.assert_called_once_with(
            self.fake_notification['event_type'], self.plugin.event_types)
        plugin.process_notification.assert_called_once_with(self.fake_notification)
        plugin._create_billing.assert_called_once_with(self.fake_notification)

