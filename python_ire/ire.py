#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

ACHAEA_ENDPOINT = 'https://api.achaea.com'


def _requires_auth(func):
    def wrapper(self, *args, **kwargs):
        if self.auth is not True:
            raise APIError()
        return func(self, *args, **kwargs)
    return wrapper


class API:

    auth = None

    CHECKAUTH_RESOURCE = '/checkauth.json'
    CHARACTERS_RESOURCE = '/characters.json'
    SPECIFIC_CHARACTER_RESOURCE = '/characters/{}.json'
    NEWS_RESOURCE = '/news.json'
    SPECIFIC_NEWS_RESOURCE = '/news/{}.json'
    SPECIFIC_NEWS_POST_RESOURCE = '/news/{}/{}.json'

    def __init__(self, endpoint=ACHAEA_ENDPOINT, username=None, password=None):
        self.endpoint = endpoint
        if username is not None and password is not None:
            self.username = username
            self.password = password
            self.checkauth()

    def _get_endpoint(self, fmt_str, args):
        return self.endpoint + fmt_str.format(*args)

    def _make_request(self, resource, args=(), authed=False, params={}):
        endpoint = self._get_endpoint(resource, args)
        auth_params = {}
        if authed:
            if self.username is None or self.password is None:
                raise APIError()
            auth_params = {'character': self.username, 'password': self.password}
        params = params.copy()
        params.update(auth_params)
        req = requests.get(endpoint, params=params)
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

    def characters(self):
        req = self._make_request(self.CHARACTERS_RESOURCE)
        if req.status_code != 200:
            return None

        result = req.json()
        characters = []
        for character in result['characters']:
            characters.append(character['name'])
        return characters

    @_requires_auth
    def _character_authed(self, character):
        req = self._make_request(self.SPECIFIC_CHARACTER_RESOURCE, (character,), True)
        if req.status_code != 200:
            return None

        result = req.json()
        return Character.parse(result)

    def _character_unauthed(self, character):
        req = self._make_request(self.SPECIFIC_CHARACTER_RESOURCE, (character,), False)
        if req.status_code != 200:
            return None

        result = req.json()
        return Character.parse(result)

    def character(self, character=None):
        if self.auth is True and (self.username == character or character is None):
            return self._character_authed(character or self.username)
        else:
            return self._character_unauthed(character)

    def sections(self):
        req = self._make_request(self.NEWS_RESOURCE, authed=self.auth)
        if req.status_code != 200:
            return None

        result = req.json()
        sections_list = map(NewsSection.parse, result)
        return sections_list

    def posts(self, section, page=None):
        params = {}
        if page is not None:
            params['page'] = page
        req = self._make_request(self.SPECIFIC_NEWS_RESOURCE, (section,), authed=self.auth,
                                 params=params)
        if req.status_code != 200:
            return None

        result = req.json()
        return result

    def post(self, section, number):
        pass


class APIError(Exception):
    pass


class Character:

    def __init__(self, name, fullname, level, house, xp_rank, player_kills, mob_kills,
                 explorer_rank, current_class, messages_total=None, messages_unread=None):
        self.name = name
        self.fullname = fullname
        self.level = level
        self.house = house
        self.xp_rank = xp_rank
        self.player_kills = player_kills
        self.mob_kills = mob_kills
        self.explorer_rank = explorer_rank
        self.current_class = current_class
        self.messages_total = messages_total
        self.messages_unread = messages_unread

    @staticmethod
    def parse(json_data):
        name = json_data['name']
        fullname = json_data['fullname']
        level = int(json_data['level'])
        house = json_data['house']
        xp_rank = json_data['xp_rank']
        player_kills = int(json_data['player_kills'])
        mob_kills = int(json_data['mob_kills'])
        explorer_rank = int(json_data['explorer_rank'])
        current_class = json_data['class']
        messages_total = None
        messages_unread = None
        if 'messages_total' in json_data and 'messages_unread' in json_data:
            messages_total = json_data['messages_total']
            messages_unread = json_data['messages_unread']

        return Character(name, fullname, level, house, xp_rank, player_kills, mob_kills,
                         explorer_rank, current_class, messages_total, messages_unread)

    def __repr__(self):
        return '<Character: {} ({})>'.format(self.name, self.fullname)


class NewsSection:

    def __init__(self, name, read, total, unread):
        self.name = name
        self.read = read
        self.total = total
        self.unread = unread

    @staticmethod
    def parse(json_data):
        name = json_data['name']
        read = int(json_data['read'])
        total = int(json_data['total'])
        unread = int(json_data['unread'])
        return NewsSection(name, read, total, unread)

    def __repr__(self):
        return '<NewsSection: {} ({}/{} unread)>'.format(self.name, self.read, self.total)
