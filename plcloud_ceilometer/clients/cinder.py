"""
# Author: Zhennan.luo(Jenner)
"""
__author__ = "Jenner.luo"

from oslo_log import log
from oslo_config import cfg
from ceilometer import keystone_client
from . import ClientBase, APIVersionManager

LOG = log.getLogger(__name__)

VERSIONS = APIVersionManager("volume", preferred_version=2)
try:
    from cinderclient.v2 import client as cinder_client_v2

    VERSIONS.load_supported_version(2, {"client": cinder_client_v2,
                                        "version": 2})
except ImportError:
    pass


class CinderClient(ClientBase):
    def __init__(self, conf=None):
        super(CinderClient, self).__init__(conf)

    def initialize_client_hook(self):
        """Initialize a Cinder client object."""
        # return cinder_client.Client(self.conf)
        api_version = VERSIONS.get_active_version()
        creds = self.conf.service_credentials
        params = {
            'session': keystone_client.get_session(self.conf),
            'endpoint_type': creds.interface,
            'region_name': creds.region_name,
            'service_type': self.conf.service_types.cinder,
        }
        return api_version['client'].Client(**params)
