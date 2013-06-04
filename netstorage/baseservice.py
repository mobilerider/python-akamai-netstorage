# coding=utf-8
# System imports
import hmac
import hashlib
from random import randint
from time import time
from urllib import urlencode

# Third party imports
import requests

# Internal imports
from .constants import AKAMAI_AUTH_VERSION


class Methods(object):
    GET = 'get'
    PUT = 'put'
    POST = 'post'
    DELETE = 'delete'


class Binding(object):
    host = None
    key = None
    key_name = None
    username = None
    password = None

    def __init__(self, host, key, key_name, username=None, password=None):
        # Unique ID guarantee uniqueness for multiple headers
        # generated at the same time for multiple requests
        self.uid = randint(1, 999999999)
        self.host = host
        self.key = key
        self.key_name = key_name
        self.username = username
        self.password = password

    @property
    def __auth_data(self):
        # X-Akamai-ACS-Auth-Data: [version], [0.0.0.0], [0.0.0.0], [time], [unique-id], [Key-name]
        return [AKAMAI_AUTH_VERSION, '0.0.0.0', '0.0.0.0', time(), self.uid, self.key_name]

    @property
    def __auth_data_as_string(self):
        return ', '.join(str(x) for x in self.__auth_data)

    def __get_sign_string(self, url, action):
        # Sign-string: URL + “\n” + “x-akamai-acs-action:” + X-Akamai-ACS-Action value + “\n”
        return '%s\nx-akamai-acs-action:%s\n' % (url, action)

    def __get_auth_sign(self, url, action):
        # Version 5 - HMAC-SHA256([key], [data] + [sign-string])
        message = '%s%s' % (self.__auth_data_as_string, self.__get_sign_string(url, action))

        return hmac.new(self.key, msg=message, digestmod=hashlib.sha256).digest().encode('base64')

    def __get_headers(self, url, action):
        return {
            'X-Akamai-ACS-Action': action,
            'X-Akamai-ACS-Auth-Data': ", ".join(self.__auth_data_as_string),
            'X-Akamai-ACS-Auth-Sign': self.__get_auth_sign(url, action)
        }

    def __get_url(self, cp_code, path):
        return '%s/%s/%s' % (self.host, cp_code, path)

    def send(self, cp_code, path, params, method=Methods.GET):
        url = self.__get_url(cp_code, path)
        action = urlencode(params)
        return requests.request(method, url, headers=self.__get_headers(url, action))

    # Helpers
    def du(self, params):
        pass