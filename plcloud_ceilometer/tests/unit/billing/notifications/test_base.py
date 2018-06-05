"""
# Author: Zhennan.luo(Jenner)
"""
__author__ = "Jenner.luo"

import mock
from plcloud_ceilometer.tests.unit import fakes
from . import FakeBillingBase, TestBase


class TestBillingBase(TestBase):
    @mock.patch('plcloudkittyclient.client._get_endpoint',
                fakes.plck_client_get_endpoint)
    @mock.patch('ceilometer.keystone_client.get_session',
                fakes.keystone_client_get_session)
    def test__process_notifications(self):
        plugin = FakeBillingBase(self.fake_manager)
        # plugin.to_samples_and_publish = mock.Mock()
        plugin._process_notifications = mock.Mock()

        plugin.info([self.fake_message])
        plugin._process_notifications.assert_called_once_with(
            'info', [self.fake_message])
