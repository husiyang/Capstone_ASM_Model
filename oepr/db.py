#!/usr/bin/env python3
"""Database"""
import os
import re
import shelve
import sys

import oepr.sample
import oepr.settings
import oepr.util


@oepr.util.check_path('f')
def _kv_write_sample(path_cfg, key, value):
    path_samples = oepr.settings.get_cfg_field('path_samples', path_cfg)

    if not os.path.isdir(path_samples):
        os.mkdir(path_samples)

    shelf = os.path.join(path_samples, key + '_shelf')

    with shelve.open(shelf) as hdl:
        hdl['metadata'] = value.pop('metadata')
        hdl['sample'] = value.pop('sample')

    print('sample written to %s' % shelf, file=sys.stderr)


@oepr.util.check_path('f')
def _kv_read_sample(path_cfg, key):
    path_samples = oepr.settings.get_cfg_field('path_samples', path_cfg)

    if not os.path.isdir(path_samples):
        raise NotADirectoryError('no such dir as %s' % path_samples)

    with shelve.open(os.path.join(path_samples, key + '_shelf')) as hdl:
        return dict(hdl)

@oepr.util.check_path('f')
def _kv_read_all_sample(path_cfg):
    path_samples = oepr.settings.get_cfg_field('path_samples', path_cfg)

    if not os.path.isdir(path_samples):
        raise NotADirectoryError('no such dir as %s' % path_samples)

    files = (
        os.path.join(path_samples, f) for f in os.listdir(path_samples)
        if os.path.isfile(os.path.join(path_samples, f))
        if f.endswith('db')
    )

    for f in files:
        k = re.match(r'^(?P<key>.*)_shelf\.db$', f).group('key')
        yield _kv_read_sample(path_cfg, k)


@oepr.util.check_path('f')
def kv_write(path_cfg, type_, key, value):
    if type_ == 'sample':
        return _kv_write_sample(path_cfg, key, value)
    else:
        raise NotImplementedError()


@oepr.util.check_path('f')
def kv_read(path_cfg, type_, key):
    if type_ == 'sample':
        return _kv_read_sample(path_cfg, key)
    else:
        raise NotImplementedError()


@oepr.util.check_path('f')
def kv_read_all(path_cfg, type_):
    if type_ == 'sample':
        return _kv_read_all_sample(path_cfg)
    else:
        raise NotImplementedError()


if __name__ == '__main__':
    pass


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
