# coding=utf-8
# System imports
import hmac
import hashlib
from random import getrandbits
from time import time

# Third party imports
from requests.auth import AuthBase

# Internal imports
from netstorage.constants import AKAMAI_AUTH_VERSION


class AkamaiAuth(AuthBase):
    """Attaches HTTP Akamai Authentication to the given Request object."""

    def __init__(self, key, key_name, url, action):
        # Unique ID guarantee uniqueness for multiple headers
        # generated at the same time for multiple requests
        self.uid = getrandbits(32)

        # setup any auth-related data
        self.key = key
        self.key_name = key_name
        self.url = url
        self.action = action

    def __call__(self, r):
        # modify and return the request
        self.__set_headers(r.headers)
        return r

    @property
    def __auth_data(self):
        # X-Akamai-ACS-Auth-Data: [version], [0.0.0.0], [0.0.0.0], [time], [unique-id], [Key-name]
        return [AKAMAI_AUTH_VERSION, '0.0.0.0', '0.0.0.0', time(), self.uid, self.key_name]

    @property
    def __auth_data_as_string(self):
        return ', '.join(str(x) for x in self.__auth_data)

    @property
    def __get_sign_string(self):
        # Sign-string: URL + “\n” + “x-akamai-acs-action:” + X-Akamai-ACS-Action value + “\n”
        return '%s\nx-akamai-acs-action:%s\n' % (self.url, self.action)

    @property
    def __get_auth_sign(self):
        message = '%s%s' % (self.__auth_data_as_string, self.__get_sign_string)

        # Version 5 - HMAC-SHA256([key], [data] + [sign-string])
        # Remove trailing \n character
        return hmac.new(self.key, msg=message, digestmod=hashlib.sha256)\
            .digest().encode('base64').replace('=\n', '=')

    def __set_headers(self, headers):
        headers['X-Akamai-ACS-Auth-Data'] = self.__auth_data_as_string
        headers['X-Akamai-ACS-Auth-Sign'] = self.__get_auth_sign
