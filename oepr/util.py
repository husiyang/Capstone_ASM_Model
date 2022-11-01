#!/usr/bin/env python3
"""
Read
"""
import functools
import os.path

import pandas as pd


def check_path(type_=None):
    if type_:
        if type_.startswith('d'):
            type_ = 'dir'
        elif type_.startswith('f'):
            type_ = 'file'
    checks = {
        'file': (os.path.isfile, FileNotFoundError),
        'dir': (os.path.isdir, NotADirectoryError)
    }
    check, err = checks.get(type_, (os.path.exists, OSError))

    def decorator_check_path(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            if not check(args[0]):
                raise err('no such file as %s' % args[0])
            return f(*args, **kwargs)
        return wrapper
    return decorator_check_path


@check_path('f')
def csv_to_dataframe(path_csv):
    return pd.read_csv(path_csv)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
