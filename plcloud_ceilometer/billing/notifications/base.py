"""
# Author: Zhennan.luo(Jenner)
"""
__author__ = "Jenner.luo"

import abc
import types
import fnmatch
import oslo_messaging
from oslo_log import log
from ceilometer import service, messaging
from ceilometer.i18n import _LE
from ceilometer.agent import plugin_base
from plcloud_ceilometer.clients.plcloudkitty import PLCloudkittyClient
from .. import EventNotificationBase

LOG = log.getLogger(__name__)


class BillingBase(EventNotificationBase):
    def __init__(self, manager):
        super(BillingBase, self).__init__(manager)
        self.hook_method = self.plcloudkitty_billing

    @abc.abstractmethod
    def process_notification(self, message):
        """Return a sequence of Counter instances for the given message.

        :param message: Message to process.
        """

    def plcloudkitty_billing(self, notification):
        print 'plcloudkitty_billing notification', notification
        if self.need_to_handle(notification['event_type'], self.event_types):
            sample = self.process_notification(notification)
            if sample:
                if type(sample) is types.GeneratorType:
                    d = sample.next()
                    sample = d.as_dict()
                return self._create_billing(sample)

    @staticmethod
    def _package_payload(message, payload):
        # NOTE(chdent): How much of the payload should we keep?
        info = {'publisher_id': message['publisher_id'],
                'timestamp': message['timestamp'],
                'event_type': message['event_type'],
                'user_id': message['payload'].get('user_id'),
                'project_id': message['payload'].get('project_id'),
                'payload': payload}
        return info

    def _create_billing(self, sample_dict):
        try:
            res = self.plcli.create_billing(sample_dict)
            LOG.info('Billing %s (%s, %s): %s',
                     sample_dict['res_type'], sample_dict['res_name'],
                     sample_dict['res_id'], res)
            return res
        except Exception as error:
            LOG.error(error)
