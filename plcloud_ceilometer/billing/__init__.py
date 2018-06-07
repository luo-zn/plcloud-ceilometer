"""
# Author: Zhennan.luo(Jenner)
"""
__author__ = "Jenner.luo"

import abc
import fnmatch
from oslo_log import log
from ceilometer.i18n import _LE
from ceilometer.agent import plugin_base
from ceilometer import messaging
from plcloud_ceilometer.clients.plcloudkitty import PLCloudkittyClient

LOG = log.getLogger(__name__)


class EventNotificationBase(plugin_base.NotificationBase):
    event_types = []

    def __init__(self, manager):
        super(EventNotificationBase, self).__init__(manager)
        self.plcli = PLCloudkittyClient(manager.conf)
        self.region_name = manager.conf.service_credentials.region_name
        self._hook_method = None

    @property
    def hook_method(self):
        return self._hook_method

    @hook_method.setter
    def hook_method(self, method):
        if callable(method):
            self._hook_method = method
        else:
            raise Exception(_LE('It Required a method!'))

    def get_targets(self, conf):
        """Return a sequence of oslo_messaging.Target

        It is defining the exchange and topics to be connected for this plugin.
        :param conf: Configuration.
        #TODO(prad): This should be defined in the notification agent
        """
        targets = []
        exchanges = [
            conf.nova_control_exchange,
            conf.cinder_control_exchange,
            conf.glance_control_exchange,
            conf.neutron_control_exchange,
            conf.heat_control_exchange,
            conf.keystone_control_exchange,
            conf.sahara_control_exchange,
            conf.trove_control_exchange,
            conf.zaqar_control_exchange,
            conf.swift_control_exchange,
            conf.ceilometer_control_exchange,
            conf.magnum_control_exchange,
            conf.dns_control_exchange,
        ]

        for exchange in exchanges:
            targets.extend(oslo_messaging.Target(topic=topic,
                                                 exchange=exchange)
                           for topic in
                           self.get_notification_topics(conf))
        return targets

    @abc.abstractmethod
    def process_notification(self, message):
        """Return a sequence of Counter instances for the given message.

        :param message: Message to process.
        """

    def _process_notifications(self, priority, notifications):
        """ This method will be called by self.info.
        :param priority:
        :param notifications:
        :return:
        """
        for notification in notifications:
            try:
                notification = messaging.convert_to_old_notification_format(
                    priority, notification)
                if self.hook_method:
                    self.hook_method(notification)
                else:
                    self.to_samples_and_publish(notification)
            except Exception:
                LOG.error(_LE('Fail to process notification'), exc_info=True)

    @staticmethod
    def need_to_handle(event_type, event_types):
        """ To check whether event_type should be handled according to event_types
        :param event_type: str
        :param event_types: list
        :return:
        """
        return any(map(lambda e: fnmatch.fnmatch(event_type, e), event_types))
