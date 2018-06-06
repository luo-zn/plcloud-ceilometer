"""
# Author: Zhennan.luo(Jenner)
"""
__author__ = "Jenner.luo"

from oslo_log import log
from oslo_config import cfg
from . import ClientBase
from ceilometer import keystone_client
from plcloudkittyclient import client as plck_client
from plcloud_ceilometer import utils

LOG = log.getLogger(__name__)


class PLCloudkittyClient(ClientBase):
    def initialize_client_hook(self):
        """Initialize a PLcloudkitty client object."""
        ks_session = keystone_client.get_session(self.conf)
        endpoint = plck_client._get_endpoint(ks_session)
        return plck_client.Client('1', endpoint, token=ks_session.get_token(),
        insecure=self.conf.service_credentials.insecure,
        cacert=getattr(self.conf.service_credentials, 'cacert', None))

    @utils.catch_log
    def get_billing(self):
        return self.client.billings.billing_manager.get_billing()

    @utils.catch_log
    def create_billing(self, data):
        return self.client.billings.billing_manager.billing_event(data)

    @utils.catch_log
    def billing_release(self, billing_id):
        self.client.billing.billing_manager.update(billing_id, status=12)

    @utils.catch_log
    def billing_update(self, billing_id, status):
        self.client.billing.billing_manager.update(billing_id, status=status)
