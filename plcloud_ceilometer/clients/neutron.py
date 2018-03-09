"""
# Author: Zhennan.luo(Jenner)
"""
__author__ = "Jenner.luo"


from oslo_log import log
from oslo_config import cfg
from . import ClientBase
from ceilometer import neutron_client

LOG = log.getLogger(__name__)


class NeutronClient(ClientBase):
    def __init__(self, conf=None):
        super(NeutronClient, self).__init__(conf)

    def initialize_client_hook(self):
        """Initialize a Neutron client object."""
        return neutron_client.Client(self.conf)

    def get_port(self, port_id):
        return self.client.show_port(port_id).get('port')

    def get_router(self, router_id):
        return self.client.show_router(router_id)

    def list_ports(self, device_id):
        return self.client.list_ports(device_id=device_id).get('ports')

    def release_ip(self, floating_ip_id):
        self.client.delete_floatingip(floating_ip_id)