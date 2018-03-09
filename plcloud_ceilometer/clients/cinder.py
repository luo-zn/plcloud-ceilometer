"""
# Author: Zhennan.luo(Jenner)
"""
__author__ = "Jenner.luo"

from oslo_log import log
from oslo_config import cfg
from . import ClientBase

LOG = log.getLogger(__name__)


class CinderClient(ClientBase):
    def __init__(self, conf=None):
        super(CinderClient, self).__init__(conf)

    def initialize_client_hook(self):
        """Initialize a Cinder client object."""
        # return cinder_client.Client(self.conf)
        return None
