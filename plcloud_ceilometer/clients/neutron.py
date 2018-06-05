"""
# Author: Zhennan.luo(Jenner)
"""
__author__ = "Jenner.luo"

import functools
from oslo_log import log
from oslo_config import cfg
from neutronclient.common import exceptions
from neutronclient.v2_0 import client as clientv20
from ceilometer import keystone_client
from . import ClientBase

LOG = log.getLogger(__name__)


def logged(func):
    @functools.wraps(func)
    def with_logging(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except exceptions.NeutronClientException as e:
            if e.status_code == 404:
                LOG.warning("The resource could not be found.")
            else:
                LOG.warning(e)
            return []
        except Exception as e:
            LOG.exception(e)
            raise


class NeutronClient(ClientBase):
    def __init__(self, conf=None):
        super(NeutronClient, self).__init__(conf)
        self.lb_version = self.conf.service_types.neutron_lbaas_version

    def initialize_client_hook(self):
        """Initialize a Neutron client object."""
        creds = self.conf.service_credentials
        params = {
            'session': keystone_client.get_session(self.conf),
            'endpoint_type': creds.interface,
            'region_name': creds.region_name,
            'service_type': self.conf.service_types.neutron,
        }
        return clientv20.Client(**params)

    @logged
    def get_all_ports(self):
        return self.client.list_ports().get('ports')

    @logged
    def get_port(self, port_id):
        return self.client.show_port(port_id).get('port')

    @logged
    def get_router(self, router_id):
        return self.client.show_router(router_id)

    @logged
    def release_ip(self, floating_ip_id):
        self.client.delete_floatingip(floating_ip_id)
