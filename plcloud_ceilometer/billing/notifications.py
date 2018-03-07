"""
# Author: Zhennan.luo(Jenner)
"""
__author__ = "Jenner.luo"

import oslo_messaging
from oslo_log import log
from ceilometer.agent import plugin_base

LOG = log.getLogger(__name__)


class ProcessBillingNotifications(plugin_base.NotificationBase):
    event_types = []

    def __init__(self, manager):
        super(ProcessBillingNotifications, self).__init__(manager)

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

    def process_notification(self, notification_body):
        print 'sssssss process_notification=', notification_body