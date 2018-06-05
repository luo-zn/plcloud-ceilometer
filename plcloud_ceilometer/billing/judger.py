"""
# Author: Zhennan.luo(Jenner)
"""
__author__ = "Jenner.luo"

import abc
from oslo_log import log
from novaclient import exceptions as nova_exceptions
from cinderclient import exceptions as cinder_exceptions
from . import EventNotificationBase
from ..clients.nova import NovaClient
from ..clients.neutron import NeutronClient
from ..clients.cinder import CinderClient

LOG = log.getLogger(__name__)


class JudgerBase(EventNotificationBase):
    def __init__(self, manager):
        super(JudgerBase, self).__init__(manager)
        self.hook_method = self.judging
        self.novaclient = NovaClient(manager)
        self.neutronclient = client.NeutronClient()
        self.cinderclient = client.CinderClient()

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
            stop_method(res_id, message['payload']['res_name'], res_type)
        else:
            LOG.error('Stop class does not implement %s method.',
                      stop_method)

    def stop_instance(self, res_id, res_name, res_type):
        LOG.info('Judge %s, stop (%s, %s).',
                 res_type, res_name, res_id)
        try:
            self.novaclient.stop(res_id)
        except Exception as error:
            LOG.error(error)


class Release(JudgerBase):
    event_types = [
        "plcloudkitty.billing.release"
    ]

    def process_notification(self, message):
        LOG.debug('Judger release notification %s', message)
        res_type = message['payload']['res_type']
        res_id = message['payload']['res_id']
        res_meta = message['payload']['res_meta']
        billing_id = message['payload']['id']
        release_method = getattr(self, "release_{}".format(res_type), None)
        if release_method:
            release_method(res_id, billing_id, res_meta)
        else:
            LOG.error('Release class does not implement %s method.',
                      stop_method)

    def release_instance(self, res_id, billing_id, *args, **kwargs):
        try:
            self.novaclient.delete(res_id)
        except nova_exceptions.NotFound:
            self.plcloudclient.billing_release(billing_id)
        except Exception as error:
            LOG.error(error)

    def release_volume(self, res_id, billing_id, *args, **kwargs):
        try:
            self.cinderclient.delete_volume(res_id)
        except cinder_exceptions.NotFound:
            self.plcloudclient.billing_release(billing_id)
        except Exception as error:
            LOG.error(error)

    def release_floatingip(self, res_id, billing_id, *args, **kwargs):
        try:
            self.neutronclient.release_ip(res_id)
        except neutron_exceptions.NotFound:
            self.plcloudclient.billing_release(billing_id)
        except Exception as error:
            LOG.error(error)

    def release_router(self, res_id, billing_id, *args, **kwargs):
        try:
            self.neutronclient.delete_router(res_id)
        except neutron_exceptions.NeutronClientException as error:
            if error.status_code == 404:
                self.plcloudclient.billing_release(billing_id)
        except Exception as error:
            LOG.error(error)

    def release_bandwidth(self, res_id, billing_id, res_meta, *args, **kwargs):
        try:
            self.neutronclient.release_bandwidth(
                res_id, res_meta['physical_network'])
            port = self.neutronclient.get_port(res_id)
            self.neutronclient.clear_gateway(port['device_id'])
        except neutron_exceptions.PortNotFoundClient:
            self.plcloudclient.billing_release(billing_id)
        except Exception as error:
            LOG.error(error)

    def release_loadbalance(self, res_id, billing_id, *args, **kwargs):
        try:
            self.neutronclient.delete_lb(res_id)
        except neutron_exceptions.NotFound:
            self.plcloudclient.billing_release(billing_id)
        except Exception as error:
            LOG.error(error)

