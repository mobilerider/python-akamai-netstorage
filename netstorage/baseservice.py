# System imports
from urllib import urlencode

# Third party imports
from netstorage.auth import AkamaiAuth
import requests


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
        self.host = host
        self.key = key
        self.key_name = key_name
        self.username = username
        self.password = password


    def __get_url(self, cp_code, path):
        return '%s/%s/%s' % (self.host, cp_code, path)

    def __get_headers(self, action):
        return {'X-Akamai-ACS-Action': action}

    def send(self, cp_code, path, params, method=Methods.GET):
        url = self.__get_url(cp_code, path)
        action = urlencode(params)

        r = requests.request(method, url, auth=AkamaiAuth(self.key, self.key_name, url, action))

        return r.text

    # Helpers
    def du(self, params):
        pass