"""
# Author: Zhennan.luo(Jenner)
"""
__author__ = "Jenner.luo"

import mock
from oslotest import base
from oslo_config import fixture as fixture_config
from plcloud_ceilometer.billing.notifications import base as plugin_base


class TestBillingBase(base.BaseTestCase):
    def setUp(self):
        super(TestBillingBase, self).setUP()
        self.CONF = self.useFixture(fixture_config.Config()).conf

        class FakeBillingBase(plugin_base.BillingBase):
            event_types = ['compute.*']

            def plcloudkitty_billing(self, notification):
                pass

            def get_targets(self, conf):
                pass

    def test_plugin_info(self):
        plugin = self.FakeBillingBase(mock.Mock())
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


