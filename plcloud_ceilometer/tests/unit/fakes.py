"""
# Author: Zhennan.luo(Jenner)
"""
__author__ = "Jenner.luo"


def plck_client_get_endpoint(*args, **kwargs):
    return "http://192.168.215.38:8899"


def keystone_client_get_session(*args, **kwargs):
    class Session(object):
        def get_token(self):
            return "4386a57966ea4ad79b48532f50812717"

    return Session()
