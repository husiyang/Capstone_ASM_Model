#!/usr/bin/env python3
"""
Preprocessing
"""
import os


def config_parser(subp):
    parse = subp.add_parser('normalise')
    parse.set_defaults(func=main)


def main(args):
    """main function for module"""
    return getattr(os, 'EX_OK', 0)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
