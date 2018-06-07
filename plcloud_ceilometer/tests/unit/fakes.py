"""
# Author: Zhennan.luo(Jenner)
"""
__author__ = "Jenner.luo"

import mock


def plck_client_get_endpoint(*args, **kwargs):
    return "http://192.168.215.38:8899"


def keystone_client_get_session(*args, **kwargs):
    class Session(object):
        def get_token(self):
            return "4386a57966ea4ad79b48532f50812717"

    return Session()


def getLogger(*args, **kwargs):
    mock_logger = mock.Mock()
    mock_logger.exception = mock.Mock()
    mock_logger.debug = mock.Mock()
    mock_logger.info = mock.Mock()
    mock_logger.error = mock.Mock()
    return mock_logger
