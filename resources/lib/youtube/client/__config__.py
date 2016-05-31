# -*- coding: utf-8 -*-
from random import randint
from base64 import b64decode
from resources.lib.kodion import Context as __Context

__context = __Context()
__settings = __context.get_settings()

version_switch = {
    '12': '0',
    '13': '0',
    '14': '1',
    '15': '2',
    '16': str(randint(3, 4)),
    '17': str(randint(4, 5))
}


def __get_key_switch():
    switch = __settings.get_string('youtube.api.key.switch', '5')
    use_switch = __settings.get_string('youtube.api.key.switch.use', '')
    if not use_switch and switch:
        major_version = __context.get_system_version().get_version()[0]
        switch = version_switch.get(str(major_version), '5')
        __settings.set_string('youtube.api.key.switch', switch)
        __settings.set_string('youtube.api.key.switch.use', switch)
        return switch
    elif use_switch != switch:
        __settings.set_string('youtube.api.key.switch.use', switch)
        return switch
    else:
        return use_switch


key_sets = {
    'own': {
        'key': __settings.get_string('youtube.api.key', '').strip(),
        'id': __settings.get_string('youtube.api.id', '').strip().replace('.apps.googleusercontent.com', ''),
        'secret': __settings.get_string('youtube.api.secret', '').strip()
    },
    'provided': {
        'switch': __get_key_switch(),
        '0': {  # Bromix youtube-for-kodi-12
            'id': 'OTQ3NTk2NzA5NDE0LTA4bnJuMzE0ZDhqM2s5MWNsNGY1MXNyY3U2bTE5aHZ1',
            'key': 'QUl6YVN5Q0RuXzlFeWJUSml5bUhpcE5TM2prNVpwQ1RYZENvdFEw',
            'secret': 'SHNMVDJaQ2V4SVYtVkZ4V2VZVloyVFVj'
        },
        '1': {  # Youtube Plugin for Kodi #1
            'id': 'Mjk0ODk5MDY0NDg4LWE4a2MxazFqZDAwa2FtcXJlMHZkMm5mdHVpaWZyZjZh',
            'key': 'QUl6YVN5Q1p3UXVvc0ZKYlF6bnFucXBxcFlsYUpXVk1uMTZ3QnZz',
            'secret': 'S1RrQktJTk41dmY0T3dqMU5ZeVhMemJl',
        },
        '2': {  # Bromix youtube-for-kodi-13
            'id': 'NDQ4OTQwNjc2NzEzLW1pbjl1NWZyZnVqcHJibmI4ZjNkcmkzY3Y5anIzMnJu',
            'key': 'QUl6YVN5QW1yZjNCbmVFUVBEaVVFdVFsenkwX3JiRkdEQmctYmkw',
            'secret': 'Nzl2TXNKc05DOWp5cFNmcnlVTXUwMGpX'
        },
        '3': {  # Bromix youtube-for-kodi-14
            'id': 'MTA3NTAwNzY3NTA2LTltdmJhYWN1c2NmOGNnZTJuM2trdmo1MGE2ZG5yazhn',
            'key': 'QUl6YVN5Q0NuWkltQzdnVG5pTmZnd3FHd2l4SWRCVkd4aUNPS2xV',
            'secret': 'MmNlVmZvZ25CQ3RuOHVoMjBIbWxKTjRY'
        },
        '4': {  # Bromix youtube-for-kodi-15
            'id': 'NjEwNjk2OTE4NzA1LWJrdDZ2NTM2azdnbjJkdGN2OHZkbmdtNGIwdnQ1c2V2',
            'key': 'QUl6YVN5QVRxRGltLTU2eThIY04xTkF6UWRWWmdkTW9jNmQ5RXlz',
            'secret': 'a1Y3UmVQMWZfTGc5aTJoV1IybGlIbk82'
        },
        '5': {  # Bromix youtube-for-kodi-16
            'id': 'ODc5NzYxNzg4MTA1LXNkdWYwaHQzMzVkdmc5MjNhbmU3Y2cxam50MWQ1bDRr',
            'key': 'QUl6YVN5QlMzck55bUp0elBZYkpYNWxTR2ROQ0JTNmFqaDRWRERZ',
            'secret': 'dkJWRGEta05kQ0hEVGtwRDhiOEhPNzE4'
        }
    }
}


def _has_own_keys():
    return False if not key_sets['own']['key'] or \
                    not key_sets['own']['id'] or \
                    not key_sets['own']['secret'] else True


has_own_keys = _has_own_keys()


def get_current_key_set():
    return 'own' if has_own_keys else key_sets['provided']['switch']


def get_last_key_set():
    return __settings.get_string('youtube.api.last', '')


def set_last_key_set(value):
    __settings.set_string('youtube.api.last', value)


def keys_changed():
    last_set = get_last_key_set()
    current_set = get_current_key_set()
    if last_set != current_set:
        set_last_key_set(current_set)
        __context.log_warning('Switching API key set from %s to %s' % (last_set, current_set))
        return True
    else:
        return False


api = {
    'key':
        key_sets['own']['key']
        if has_own_keys
        else
        b64decode(key_sets['provided'][key_sets['provided']['switch']]['key']),
    'id':
        '%s.apps.googleusercontent.com' %
        (key_sets['own']['id']
         if has_own_keys
         else
         b64decode(key_sets['provided'][key_sets['provided']['switch']]['id'])),
    'secret':
        key_sets['own']['secret']
        if has_own_keys
        else
        b64decode(key_sets['provided'][key_sets['provided']['switch']]['secret'])
}
