#!/usr/bin/env python3
"""
Learn
"""
import os


def config_parser(subp):
    parse = subp.add_parser('learn')
    parse.set_defaults(func=main)
    return parse


def learn():
    print('learn')


def main(args):
    learn()

    return getattr(os, 'EX_OK', 0)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
