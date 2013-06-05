# System imports
from urllib import urlencode
from xml.etree.ElementTree import fromstring

# Third party imports
import requests

# Internal imports
from netstorage.auth import AkamaiAuth
from netstorage.exception import *


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


class Actions(object):
    DU = 'du'


class Binding(object):
    host = None
    key = None
    key_name = None
    username = None
    password = None
    cp_code = None

    def __init__(self, host, key, key_name, cp_code=None, username=None, password=None):
        self.host = host
        self.key = key
        self.key_name = key_name
        self.cp_code = cp_code
        self.username = username
        self.password = password

        # To ensure you will not delete a content by mistake
        # Call allow_delete method before requesting a delete action
        self.allow_delete = False


    def __get_url(self, cp_code, path):
        url = 'http://%s/%s/%s' % (self.host, cp_code, path)

        # Ensures that there is no trailing slash
        return url if url[-1:] != '/' else url[:-1]

    def __get_relative_url(self, cp_code, path):
        relative = '/%s/%s' % (cp_code, path)

        # Ensures that there is no trailing slash
        return relative if relative[-1:] != '/' else relative[:-1]

    def __get_headers(self, action):
        return {
            'Host': self.host,
            'X-Akamai-ACS-Action': action
        }

    def send(self, cp_code, path, params, method=Methods.GET):
        cp_code = cp_code or self.cp_code
        url = self.__get_url(cp_code, path)
        relative = self.__get_relative_url(cp_code, path)
        action = urlencode(params)

        try:
            cp_code = int(cp_code)
            assert cp_code >= 0
        except (TypeError, AssertionError):
            raise AkamaiInvalidCpCodeException()

        if not Methods.validate_method(method):
            raise AkamaiInvalidMethodException()

        if method == Methods.DELETE and not self.allow_delete:
            raise AkamaiDeleteNotAllowedException()

        r = requests.request(method, url, headers=self.__get_headers(action),
                             auth=AkamaiAuth(self.key, self.key_name, relative, action))

        return r.text, r.status_code

    def allow_deleting(self):
        self.allow_delete = True

    # Helpers
    def du(self, cp_code, path, params=None):
        params['action'] = Actions.DU

        # Making the request
        response, status = self.send(cp_code, path, params)

        if status == 200:
            try:
                tree = fromstring(response)
                info = tree.find('du-info').attrib
                return {'files': info['files'], 'bytes': info['bytes']}
            except Exception:
                raise AkamaiResponseMalformedException()
        else:
            return response