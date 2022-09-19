#!/usr/bin/env python3
"""
Read
"""
import os.path
import csv

import oepr.util

KEY_TOTAL_FRAMES = 'Total Frames in Take'


def _parse_data_line(line):
    """parse data line"""
    data = line.strip().split(',')

    frame = data.pop(0)
    time = data.pop(0)

    return {
        'frame': int(frame),
        'time': float(time),
        'points': [
            (float(data[3 * k]), float(data[3 * k + 1]), float(data[3 * k + 2]))
            for k in range(len(data) // 3)
        ]
    }


@oepr.util.check_path('f')
def get_info_take(path_csv):
    """Get the basic information about a take"""
    with open(path_csv, 'r') as hdl:
        data = next(hdl).split(',')

    info = {
        data[2 * k].strip(): data[2 * k + 1].strip()
        for k in range(len(data) // 2)
    }
    info[KEY_TOTAL_FRAMES] = int(info[KEY_TOTAL_FRAMES])
    info['Total Exported Frames'] = int(info['Total Exported Frames'])
    info['Export Frame Rate'] = float(info['Export Frame Rate'])

    assert info[KEY_TOTAL_FRAMES] == info['Total Exported Frames']

    return info


@oepr.util.check_path('f')
def get_data_take(path_csv):
    """Get a take's data"""
    with open(path_csv, 'r') as hdl:
        # skip down to position information
        for line in hdl:
            if line.startswith('Frame'):
                break

        for line in hdl:
            yield _parse_data_line(line)


@oepr.util.check_path('d')
def get_csvs(path_labelled_visits):
    files = (
        os.path.join(dirpath, f)
        for dirpath, _, filenames in os.walk(path_labelled_visits)
        for f in filenames
        if 'NIDAQ' not in f
        if f.endswith('csv')
    )
    for f in files:
        yield f


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
