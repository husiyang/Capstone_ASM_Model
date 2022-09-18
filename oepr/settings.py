#!/usr/bin/env python3
"""
Settings
"""
import json
import os


BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_SETTINGS_FILENAME = 'settings.json'
DEFAULT_SETTINGS_PATH = os.path.join(BASE, DEFAULT_SETTINGS_FILENAME)
DEFAULT_SETTINGS = {
    'path_labelled_visits': '/path/to/visits',
}


def create_default_settings(name_file=DEFAULT_SETTINGS_FILENAME):
    """create default settings file"""
    path_file = os.path.join(BASE, name_file)

    if os.path.isfile(path_file):
        raise RuntimeError('settings file %s already exists' % path_file)

    with open(path_file, 'w') as hdl:
        json.dump(DEFAULT_SETTINGS, hdl, sort_keys=True, indent=4)


def get_cfg_field(field, path_file=DEFAULT_SETTINGS_PATH, converter=str):
    """get configuration field"""
    with open(path_file, 'r') as hdl:
        return converter(json.load(hdl).get(field))


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
