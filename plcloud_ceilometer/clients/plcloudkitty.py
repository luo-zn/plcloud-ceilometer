"""
# Author: Zhennan.luo(Jenner)
"""
__author__ = "Jenner.luo"

from oslo_log import log
from oslo_config import cfg
from . import ClientBase
from ceilometer import keystone_client
from plcloudkittyclient import client as plck_client

OPTS = [
    cfg.BoolOpt('plcloudkitty_http_log_debug',
                default=False,
                deprecated_for_removal=True,
                help=('Allow plcloudkittyclient\'s debug log output. '
                      '(Use default_log_levels instead)')),
]

SERVICE_OPTS = [
    cfg.StrOpt('plcloudkitty',
               default='plcloudkitty',
               help='plcloudkitty service type.'),
]
CONF = cfg.CONF
CONF.set_default(OPTS)
CONF.register_opts(SERVICE_OPTS, group='service_types')

LOG = log.getLogger(__name__)


class PLClient(object):
    """A client which gets information via python-plcloudkittyclient."""

    def __init__(self, conf):
        """Initialize a nova client object."""
        creds = conf.service_credentials
        logger = None
        if conf.plcloudkitty_http_log_debug:
            logger = log.getLogger("plcloudkittyclient-debug")
            logger.logger.setLevel(log.DEBUG)
        ks_session = keystone_client.get_session(conf)
        self.plck_client = plck_client.Client(
            version='1',
            session=ks_session,

            # adapter options
            region_name=creds.region_name,
            endpoint_type=creds.interface,
            service_type=conf.service_types.plcloudkitty,
            logger=logger)


class PLCloudkittyClient(ClientBase):
    def initialize_client_hook(self):
        """Initialize a PLcloudkitty client object."""
        return plck_client.Client('1', endpoint, **kwargs)

    def get_billing(self):
        return self.client.billings.billing_manager.get_billing()

    def create_billing(self, data):
        return self.client.billings.billing_manager.billing_event(data)

    def billing_release(self, billing_id):
        self.client.billing.billing_manager.update(billing_id, status=12)

    def billing_update(self, billing_id, status):
        self.client.billing.billing_manager.update(billing_id, status=status)
