"""
# Author: Zhennan.luo(Jenner)
"""
__author__ = "Jenner.luo"

from oslo_log import log
from oslo_config import cfg
from ceilometer import keystone_client
from . import ClientBase, APIVersionManager
from plcloud_ceilometer.utils.decorators import catch_log

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

    @catch_log
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

    @catch_log
    def get_all_volume(self):
        search_opts = {'all_tenants': True}
        return self.client.volumes.list(True, search_opts)

    @catch_log
    def get_volume(self, volume_id):
        return self.client.volumes.get(volume_id)

    @catch_log
    def delete_volume(self, volume_id):
        volume = self.get_volume(volume_id)
        if volume.status == 'in-use':
            volume.detach()
        a = lambda x: x.volume_id == volume_id
        snapshots = filter(a, self.client.volume_snapshots.list(
            search_opts={'all_tenants': True}))
        for i in snapshots:
            # fix me: snapshot may have volume
            self.client.volume_snapshots.delete(i.id)
        return volume.delete()

