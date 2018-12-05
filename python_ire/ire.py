#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

ACHAEA_ENDPOINT = 'https://api.achaea.com'


class API:

    auth = None

    CHECKAUTH_RESOURCE = '/checkauth.json'
    CHARACTERS_RESOURCE = '/characters.json'
    SPECIFIC_CHARACTER_RESOURCE = '/characters/{}.json'

    def __init__(self, endpoint=ACHAEA_ENDPOINT, character=None, password=None):
        if character is not None and password is not None:
            self.character = character
            self.password = password

        self.endpoint = endpoint

    def _requires_auth(self, func):
        def wrapper(*args, **kwargs):
            if self.auth is not True:
                raise APIError()
            return func(*args, **kwargs)
        return wrapper

    def _get_endpoint(self, fmt_str, args):
        return self.endpoint + fmt_str.format(args)

    def _make_request(self, resource, args=(), authed=False):
        endpoint = self._get_endpoint(resource, args)
        auth_params = {}
        if authed:
            if self.character is None or self.password is None:
                raise APIError()
            auth_params = {'character': self.character, 'password': self.password}
        req = requests.get(endpoint, params=auth_params)
        return req

    def checkauth(self):
        if self.auth is not None:
            return self.auth

        req = self._make_request(self.CHECKAUTH_RESOURCE, authed=True)

        if req.status_code == 200:
            self.auth = True
        else:
            self.auth = False

        return self.auth

    def _characters_auth(self):
        pass

    def _characters_unauth(self):
        req = self._make_request(self.CHARACTERS_RESOURCE)
        if req.status_code == 200:
            return req.json()

    def characters(self):
        if self.auth is True:
            return self._characters_auth()
        else:
            return self._characters_unauth()


class APIError(Exception):
    pass
