"""
# Author: Zhennan.luo(Jenner)
"""
__author__ = "Jenner.luo"

import oslo_messaging
from oslo_log import log
from ceilometer import service, messaging
from ceilometer.i18n import _LE
from ceilometer.agent import plugin_base
from plcloud_ceilometer.clients.plcloudkitty import PLCloudkittyClient

LOG = log.getLogger(__name__)


class BillingBase(plugin_base.NotificationBase):
    event_types = []

    def __init__(self, manager):
        super(BillingBase, self).__init__(manager)
        # self.conf = service.prepare_service()
        # self.plcli = PLCloudkittyClient(self.conf)

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

    # def _process_notifications(self, priority, notifications):
    #     for notification in notifications:
    #         try:
    #             print 'before convert notification=', notifications
    #             notification = messaging.convert_to_old_notification_format(
    #                 priority, notification)
    #             print 'after convert notification=', notifications
    #             self.to_samples_and_publish(notification)
    #         except Exception:
    #             LOG.error(_LE('Fail to process notification'), exc_info=True)

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