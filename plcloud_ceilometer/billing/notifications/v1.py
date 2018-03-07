"""
# Author: Zhennan.luo(Jenner)
"""
__author__ = "Jenner.luo"

import oslo_messaging
from oslo_log import log
from ceilometer.i18n import _
from .base import BillingBase

LOG = log.getLogger(__name__)


class Instance(BillingBase):
    event_types = ["compute.instance.*"]

    def get_targets(self, conf):
        """oslo.messaging.TargetS for this plugin."""
        return [oslo_messaging.Target(topic=topic,
                                      exchange=conf.nova_control_exchange)
                for topic in self.get_notification_topics(conf)]

    def process_notification(self, message):
        print 'Instance notification=', message
        LOG.debug(_('Instance notification %r') % message)
        user_id = message['payload']['user_id']
        tenant_id = message['payload']['tenant_id']
        res_id = message['payload']['instance_id']
        res_name = message['payload']['display_name']
        res_type = 'instance'
        message_id = message['message_id']
        timestamp = message['timestamp']
        event_type = message['event_type']
        res_meta = {'memory_gb': message['payload']['memory_mb'] / 1024,
                    'vcpus': message['payload']['vcpus'],
                    'disk_gb': message['payload']['disk_gb'],
                    'ephemeral_gb': message['payload']['ephemeral_gb']}
        return {'message_id': message_id,
                'res_id': res_id,
                'res_name': res_name,
                'res_meta': res_meta,
                'res_type': res_type,
                'event_type': event_type,
                'timestamp': timestamp,
                'user_id': user_id,
                'tenant_id': tenant_id}


class Volume(BillingBase):
    event_types = [
        "volume.create.end",
        "volume.delete.end",
        "volume.resize.end",
    ]

    def get_targets(self, conf):
        """oslo.messaging.TargetS for this plugin."""
        return [oslo_messaging.Target(topic=topic,
                                      exchange=conf.cinder_control_exchange)
                for topic in self.get_notification_topics(conf)]

    def process_notification(self, message):
        print 'Volume notification=', message
        LOG.debug(_('Volume notification %r') % message)
        user_id = message['payload']['user_id']
        tenant_id = message['payload']['tenant_id']
        res_id = message['payload']['volume_id']
        res_name = message['payload']['display_name']
        res_type = 'volume'
        message_id = message['message_id']
        timestamp = message['timestamp']
        event_type = message['event_type']
        res_meta = {'volume_gb': message['payload']['size']}
        return {'message_id': message_id,
                'res_id': res_id,
                'res_name': res_name,
                'res_meta': res_meta,
                'res_type': res_type,
                'event_type': event_type,
                'timestamp': timestamp,
                'user_id': user_id,
                'tenant_id': tenant_id}
