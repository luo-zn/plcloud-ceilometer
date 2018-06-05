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

    def register_service_credentials(self):
        group = "service_credentials"
        self.CONF.register_opts([cfg.StrOpt(
            'region_name', default="FakeRegion",help="Fake Region Name"),
            cfg.BoolOpt('insecure', default=False, help="Fake insecure"),
        ],group=group)

    @property
    def fake_manager(self):
        manager = mock.Mock()
        manager.conf = self.CONF
        return manager

    class FakeBillingBase(plugin_base.BillingBase):
        event_types = ['compute.*']

        def process_notification(self, message):
            pass

        def plcloudkitty_billing(self, notification):
            pass

    @mock.patch('plcloudkittyclient.client._get_endpoint',
                fakes.plck_client_get_endpoint)
    @mock.patch('ceilometer.keystone_client.get_session',
                fakes.keystone_client_get_session)
    def test_plugin_info(self):
        plugin = self.FakeBillingBase(self.fake_manager)
        # plugin.to_samples_and_publish = mock.Mock()
        plugin.plcloudkitty_billing = mock.Mock()
        message = {
            'ctxt': {'user_id': 'fake_user_id',
                     'project_id': 'fake_project_id'},
            'publisher_id': 'fake.publisher_id',
            'event_type': 'fake.event',
            'payload': {'foo': 'bar'},
            'metadata': {'message_id': '3577a84f-29ec-4904-9566-12c52289c2e8',
                         'timestamp': '2015-06-1909:19:35.786893'}
        }
        plugin.info([message])
        notification = {
            'priority': 'info',
            'event_type': 'fake.event',
            'timestamp': '2015-06-1909:19:35.786893',
            '_context_user_id': 'fake_user_id',
            '_context_project_id': 'fake_project_id',
            'publisher_id': 'fake.publisher_id',
            'payload': {'foo': 'bar'},
            'message_id': '3577a84f-29ec-4904-9566-12c52289c2e8'
        }
        print dir(plugin.plcloudkitty_billing)
        plugin.plcloudkitty_billing.assert_called_with(notification)
        plugin.plcloudkitty_billing.assert_called_once_with(notification)


