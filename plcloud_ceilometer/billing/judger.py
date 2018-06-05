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
        # if not cfg.CONF.plcloud.enable_judger:
        #     LOG.info('Oh, oh! Judger is disabled.')
        #     return
        if self.need_to_handle(notification['event_type'], self.event_types):
            pass