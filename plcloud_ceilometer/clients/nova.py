"""
# Author: Zhennan.luo(Jenner)
"""
__author__ = "Jenner.luo"

from oslo_log import log
from oslo_config import cfg
from . import ClientBase
from ceilometer import nova_client

LOG = log.getLogger(__name__)


class NovaClient(ClientBase):
    def __init__(self, conf=None):
        super(NovaClient, self).__init__(conf)

    def initialize_client_hook(self):
        """Initialize a Nova client object."""
        return nova_client.Client(self.conf)

    def create_image(self, instance_id, name):
        self.client.servers.create_image(instance_id, name)

    def get_instance(self, instance_id):
        inst = self.client.servers.get(instance_id)
        addresses = [i['addr'] for i in chain(*inst.addresses.values())]
        return {
            'addresses': addresses,
            'user_id': inst.user_id,
            'instance_name': inst.name
        }

    def get_all_instance(self):
        search_opts = {'all_tenants': True}
        return self.client.servers.list(True, search_opts)

    def confirm_resize(self, instance_id):
        self.client.servers.confirm_resize(instance_id)

    def stop(self, instance_id):
        self.client.servers.stop(instance_id)

    def delete(self, instance_id):
        self.client.servers.delete(instance_id)