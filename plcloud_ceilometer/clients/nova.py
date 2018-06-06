"""
# Author: Zhennan.luo(Jenner)
"""
__author__ = "Jenner.luo"

from itertools import chain
from oslo_log import log
from oslo_config import cfg
from novaclient import api_versions
from novaclient import client as nova_client
from ceilometer import keystone_client
from . import ClientBase

LOG = log.getLogger(__name__)


class NovaClient(ClientBase):
    def __init__(self, conf=None):
        super(NovaClient, self).__init__(conf)

    def initialize_client_hook(self):
        """Initialize a Nova client object."""
        creds = self.conf.service_credentials
        logger = None
        if self.conf.nova_http_log_debug:
            logger = log.getLogger("novaclient-debug")
            logger.logger.setLevel(log.DEBUG)
        ks_session = keystone_client.get_session(self.conf)
        return nova_client.Client(
            version=api_versions.APIVersion('2.1'),
            session=ks_session,
            # nova adapter options
            region_name=creds.region_name,
            endpoint_type=creds.interface,
            service_type=self.conf.service_types.nova,
            logger=logger)

    def get_instance(self, instance_id):
        inst = self.client.servers.get(instance_id)
        addresses = [i['addr'] for i in chain(*inst.addresses.values())]
        inst.ips = addresses
        return inst

    def get_all_instance(self):
        search_opts = {'all_tenants': True}
        return self.client.servers.list(True, search_opts)

    def confirm_resize(self, instance_id):
        self.client.servers.confirm_resize(instance_id)

    def stop(self, instance_id):
        self.client.servers.stop(instance_id)

    def delete(self, instance_id):
        self.client.servers.delete(instance_id)

    def create_image(self, instance_id, name):
        self.client.servers.create_image(instance_id, name)