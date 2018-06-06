"""
# Author: Zhennan.luo(Jenner)
"""
__author__ = "Jenner.luo"


def catch_log(func):
    from oslo_log import log
    LOG = log.getLogger(__name__)

    def logging(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            LOG.exception(e)
            raise

    return logging
