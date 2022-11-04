#!/usr/bin/env python3
"""
Notebook.
"""
import os
import subprocess
import sys

import oepr.settings


def config_parser(subp):
    parse = subp.add_parser('notebook', help='helper to run notebook')
    parse.set_defaults(func=main)
    return parse


def main(args):
    """main function for module"""
    path_cfg = args.config_file
    path_notebook = oepr.settings.get_cfg_field('path_notebook', path_cfg)

    if not os.path.isfile(path_notebook):
        print('no such path as %s' % path_notebook, file=sys.stderr)
        return -1

    proc = subprocess.run(['jupyter', 'notebook', path_notebook], check=True)

    return proc.returncode or getattr(os, 'EX_OK', 0)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
