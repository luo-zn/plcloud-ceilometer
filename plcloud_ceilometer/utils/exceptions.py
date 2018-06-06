"""
# Author: Zhennan.luo(Jenner)
"""
__author__ = "Jenner.luo"

import logging

LOG = logging.getLogger(__name__)


class BaseException(Exception):
    """Base exception class for distinguishing our own exception classes."""
    pass


class ConfigurationError(BaseException):
    """Exception to be raised when invalid config have been provided."""
    pass
