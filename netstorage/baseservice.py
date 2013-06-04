# System imports
from urllib import urlencode

# Third party imports
from netstorage.auth import AkamaiAuth
from netstorage.exception import AkamaiInvalidMethodException, AkamaiDeleteNotAllowedException
import requests


class Methods(object):
    GET = 'GET'
    PUT = 'PUT'
    POST = 'POST'
    DELETE = 'DELETE'

    @staticmethod
    def get_methods():
        return [x for x in dir(Methods) if '_' not in x]

    @staticmethod
    def validate_method(method):
        return method in Methods.get_methods()


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

        # To ensure you will not delete a content by mistake
        # Call allow_delete method before requesting a delete action
        self.allow_delete = False


    def __get_url(self, cp_code, path):
        return 'http://%s/%s/%s' % (self.host, cp_code, path)

    def __get_headers(self, action):
        return {
            'Host': self.host,
            'X-Akamai-ACS-Action': action
        }

    def send(self, cp_code, path, params, method=Methods.GET):
        url = self.__get_url(cp_code, path)
        action = urlencode(params)

        if not Methods.validate_method(method):
            raise AkamaiInvalidMethodException()

        if method == Methods.DELETE and not self.allow_delete:
            raise AkamaiDeleteNotAllowedException()

        r = requests.request(method, url, headers=self.__get_headers(action),
                             auth=AkamaiAuth(self.key, self.key_name, url, action))

        return r.text

    def allow_deleting(self):
        self.allow_delete = True

    # Helpers
    def du(self, params):
        pass