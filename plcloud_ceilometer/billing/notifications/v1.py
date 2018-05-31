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
    event_types = [
        "compute.instance.create.end",
        "compute.instance.power_off.end",
        "compute.instance.power_on.end",
        "compute.instance.delete.end",
        "compute.instance.resize.confirm.end",
        "compute.instance.reboot.end",
    ]

    def get_targets(self, conf):
        """oslo.messaging.TargetS for this plugin."""
        return [oslo_messaging.Target(topic=topic,
                                      exchange=conf.nova_control_exchange)
                for topic in self.get_notification_topics(conf)]

    def process_notification(self, message):
        LOG.debug(_('Instance notification %r') % message)
        # user_id = message['payload']['user_id']
        # tenant_id = message['payload']['tenant_id']
        # resource_id = message['payload']['instance_id']
        # res_name = message['payload']['display_name']
        # res_type = 'instance'
        # timestamp = message['timestamp']
        # res_meta = {'memory_gb': message['payload']['memory_mb'] / 1024,
        #             'vcpus': message['payload']['vcpus'],
        #             'disk_gb': message['payload']['disk_gb'],
        #             'ephemeral_gb': message['payload']['ephemeral_gb']}
        # info = self._package_payload(message, message['payload'])
        # yield sample.Sample.from_notification(
        #     name='%s.%s' % (message['event_type'], res_name),
        #     type=res_type,
        #     unit=message['event_type'].split('.')[1],
        #     volume=volume,
        #     resource_id=resource_id,
        #     message=info,
        #     user_id=user_id,
        #     project_id=tenant_id,
        #     timestamp=timestamp, metadata=res_meta)
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
                'project_id': tenant_id}


class Image(BillingBase):
    event_types = [
        "compute.instance.create.end",
        "compute.instance.delete.end",
    ]

    def get_targets(self, conf):
        """oslo.messaging.TargetS for this plugin."""
        return [oslo_messaging.Target(topic=topic,
                                      exchange=conf.glance_control_exchange)
                for topic in self.get_notification_topics(conf)]

    def process_notification(self, message):
        LOG.debug(_('Image notification %r') % message)
        user_id = message['payload']['user_id']
        tenant_id = message['payload']['tenant_id']
        res_id = '%s_%s' % (message['payload']['image_meta']['image_id'],
                            message['payload']['instance_id'])
        res_name = message['payload']['image_meta']['image_name']
        res_type = 'image'
        # same as the instance message_id
        message_id = message['message_id']
        timestamp = message['timestamp']
        event_type = message['event_type']
        res_meta = {
            'architecture': message['payload']['image_meta']['architecture'],
            'os_distro': message['payload']['image_meta']['os_distro'],
            'os_version': message['payload']['image_meta']['os_version'],
            'vol_size': message['payload']['image_meta']['vol_size'],
            message['payload']['image_meta']['image_id']: 1}
        return {'message_id': message_id,
                'res_id': res_id,
                'res_name': res_name,
                'res_meta': res_meta,
                'res_type': res_type,
                'event_type': event_type,
                'timestamp': timestamp,
                'user_id': user_id,
                'project_id': tenant_id}


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
        user_id = message['payload']['user_id']
        project_id = message['payload']['tenant_id']
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
                "region": self.region_name,
                'project_id': project_id}


class Router(BillingBase):
    event_types = [
        "router.create.end",
        "router.delete.end",
    ]

    def get_targets(self, conf):
        """oslo.messaging.TargetS for this plugin."""
        return [oslo_messaging.Target(topic=topic,
                                      exchange=conf.neutron_control_exchange)
                for topic in self.get_notification_topics(conf)]

    def process_notification(self, message):
        LOG.debug(_('Router notification %r') % message)
        res_type = 'router'
        message_id = message['message_id']
        timestamp = message['timestamp']
        user_id = message['context']['user_id']
        tenant_id = message['payload']['tenant_id']
        event_type = message['event_type']
        res_meta = {'router': 1}
        res_id = message['payload']['id']
        res_name = message['payload']['name']
        return {'message_id': message_id,
                'res_id': res_id,
                'res_name': res_name,
                'res_meta': res_meta,
                'res_type': res_type,
                'event_type': event_type,
                'timestamp': timestamp,
                'user_id': user_id,
                'project_id': tenant_id}


class FloatingIP(BillingBase):
    event_types = [
        "floatingip.create.end",
        "floatingip.delete.end",
    ]

    def get_targets(self, conf):
        """oslo.messaging.TargetS for this plugin."""
        return [oslo_messaging.Target(topic=topic,
                                      exchange=conf.cinder_control_exchange)
                for topic in self.get_notification_topics(conf)]

    def process_notification(self, message):
        LOG.debug(_('FloatingIp notification %r') % message)
        event_type = message['event_type']
        message_id = message['message_id']
        timestamp = message['timestamp']
        res_type = 'floatingip'
        res_name = message['payload']['floating_ip_address']
        res_meta = {'floatingip': 1}
        res_id = message['payload']['id']
        user_id = message['context']['user_id']
        tenant_id = message['payload']['tenant_id']

        return {'message_id': message_id,
                'res_id': res_id,
                'res_name': res_name,
                'res_meta': res_meta,
                'res_type': res_type,
                'event_type': event_type,
                'timestamp': timestamp,
                'user_id': user_id,
                'project_id': tenant_id}
