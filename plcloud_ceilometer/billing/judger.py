"""
# Author: Zhennan.luo(Jenner)
"""
__author__ = "Jenner.luo"

import abc
from oslo_log import log
from . import EventNotificationBase

LOG = log.getLogger(__name__)


class JudgerBase(EventNotificationBase):
    def __init__(self, manager):
        super(JudgerBase, self).__init__(manager)
        self.hook_method = self.judging
        # self.novaclient = client.NovaClient()
        # self.neutronclient = client.NeutronClient()
        # self.cinderclient = client.CinderClient()
        # self.plcloudclient = client.PlcloudClient()

    def get_targets(self, conf):
        """oslo.messaging.TargetS for this plugin."""
        return [oslo_messaging.Target(topic=topic + ".info",
                                      exchange=conf.keystone_control_exchange)
                for topic in self.get_notification_topics(conf)]

    @abc.abstractmethod
    def process_notification(self, message):
        pass

    def judging(self, notification):
        if self.need_to_handle(notification['event_type'], self.event_types):
            return self.process_notification(notification)


class Stop(JudgerBase):
    event_types = [
        "plcloudkitty.billing.stop"
    ]

    def process_notification(self, message):
        LOG.debug('Judger stop notification %s', message)
        res_type = message['payload']['res_type']
        res_id = message['payload']['res_id']
        stop_method = getattr(self, "stop_{}".format(res_type), None)
        if stop_method:
            stop_method(res_id,message['payload']['res_name'],res_type)
        else:
            LOG.error('Stop class does not implement %s method.', stop_method)

    def stop_instance(self, res_id, res_name, res_type):
        LOG.info('Judge %s, stop (%s, %s).',
                 res_type, res_name, res_id)
        try:
            self.novaclient.stop(res_id)
        except Exception as error:
            LOG.error(error)

