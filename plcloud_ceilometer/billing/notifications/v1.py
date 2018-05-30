"""
# Author: Zhennan.luo(Jenner)
"""
__author__ = "Jenner.luo"

import oslo_messaging
from oslo_log import log
from ceilometer.i18n import _
from ceilometer import sample
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
        LOG.debug(_('Instance notification %r') % message)
        user_id = message['payload']['user_id']
        tenant_id = message['payload']['tenant_id']
        resource_id = message['payload']['instance_id']
        res_name = message['payload']['display_name']
        res_type = 'instance'
        timestamp = message['timestamp']
        res_meta = {'memory_gb': message['payload']['memory_mb'] / 1024,
                    'vcpus': message['payload']['vcpus'],
                    'disk_gb': message['payload']['disk_gb'],
                    'ephemeral_gb': message['payload']['ephemeral_gb']}
        info = self._package_payload(message, message['payload'])
        yield sample.Sample.from_notification(
            name='%s.%s' % (message['event_type'], res_name),
            type=res_type,
            unit=message['event_type'].split('.')[1],
            volume=volume,
            resource_id=resource_id,
            message=info,
            user_id=user_id,
            project_id=tenant_id,
            timestamp=timestamp, metadata=res_meta)


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
        LOG.debug(_('Volume notification %r') % message)
        # user_id = message['payload']['user_id']
        # tenant_id = message['payload']['tenant_id']
        # resource_id = message['payload']['volume_id']
        # res_name = message['payload']['display_name']
        # res_type = 'volume'
        # timestamp = message['timestamp']
        # res_meta = {'volume_gb': message['payload']['size']}
        # info = self._package_payload(message, message['payload'])
        # yield sample.Sample.from_notification(
        #     name='%s.%s' % (message['event_type'], res_name),
        #     type=res_type,
        #     unit='GB',
        #     volume=message['payload']['size'],
        #     resource_id=resource_id,
        #     message=info,
        #     user_id=user_id,
        #     project_id=tenant_id,
        #     timestamp=timestamp,metadata=res_meta)
        return {"res_id": message["_context_request_id"],
         "res_name": message["payload"]["display_name"],
         "res_meta": message['payload'],
         "res_type": message['event_type'].split(".")[0],
         "user_id": message['payload']['user_id'],
         "region": self.region_name,
         "message_id": message['message_id'],
         "event_type": message['event_type']}
