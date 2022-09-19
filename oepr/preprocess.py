#!/usr/bin/env python3
"""
Preprocessing
"""
import collections
import random

import oepr.util
import oepr.read

DEFAULT_SAMPLE_SIZE = 100


@oepr.util.check_path('f')
def sample_random(path_csv, size=DEFAULT_SAMPLE_SIZE):
    count_frames = oepr.read.get_info_take(path_csv)[oepr.read.KEY_TOTAL_FRAMES]

    random_indices = random.sample(range(count_frames) , k=size)
    random_indices = sorted(random_indices)
    random_indices = collections.deque(random_indices)

    current_index = random_indices.popleft()

    for d in oepr.read.get_data_take(path_csv):
        if d['frame'] == current_index:
            yield d
            try:
                current_index = random_indices.popleft()
            except IndexError:
                break


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
