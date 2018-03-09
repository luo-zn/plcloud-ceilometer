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


LOG = log.getLogger(__name__)


@six.add_metaclass(abc.ABCMeta)
class ClientBase(object):
    def __init__(self, conf=None):
        self.conf = conf or cfg.CONF
        self.client = self.initialize_client_hook()

    @abc.abstractmethod
    def initialize_client_hook(self):
        '''initialize_client_hook'''
