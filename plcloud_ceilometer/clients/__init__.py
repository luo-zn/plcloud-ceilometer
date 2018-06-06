# -*- encoding: utf-8 -*-
"""
# Author: Zhennan.luo(Jenner)
# API客户端
"""
__author__ = "Jenner.luo"

import abc
import six
from oslo_log import log
from oslo_config import cfg
from plcloud_ceilometer import exceptions

LOG = log.getLogger(__name__)


@six.add_metaclass(abc.ABCMeta)
class ClientBase(object):
    def __init__(self, conf=None):
        self.conf = conf or cfg.CONF
        self.client = self.initialize_client_hook()

    @abc.abstractmethod
    def initialize_client_hook(self):
        '''initialize_client_hook'''


class APIVersionManager(object):
    """Object to store and manage API versioning data and utility methods."""
    OPENSTACK_API_VERSIONS = {}

    def __init__(self, service_type, preferred_version=None):
        self.service_type = service_type
        self.preferred = preferred_version
        self._active = None
        self.supported = {}
        if self.preferred:
            self.supported[self.preferred] = {"version": self.preferred}

    @property
    def active(self):
        if self._active is None:
            self.get_active_version()
        return self._active

    def load_supported_version(self, version, data):
        self.supported[version] = data

    def get_active_version(self):
        if self._active is not None:
            return self.supported[self._active]
        key = self.OPENSTACK_API_VERSIONS.get(self.service_type)
        if key is None:
            key = self.preferred
        # Since we do a key lookup in the supported dict the type matters,
        # let's ensure people know if they use a string when the key isn't.
        if isinstance(key, six.string_types):
            msg = ('The version "%s" specified for the %s service should be '
                   'either an integer or a float, not a string.' %
                   (key, self.service_type))
            raise exceptions.ConfigurationError(msg)
        # Provide a helpful error message if the specified version isn't in the
        # supported list.
        if key not in self.supported:
            choices = ", ".join(str(k) for k in six.iterkeys(self.supported))
            msg = ('%s is not a supported API version for the %s service, '
                   ' choices are: %s' % (key, self.service_type, choices))
            raise exceptions.ConfigurationError(msg)
        self._active = key
        return self.supported[self._active]

    def clear_active_cache(self):
        self._active = None
