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
def sample_average_bucketed_centroid_distance(path_csv,
        size=DEFAULT_SAMPLE_SIZE, **kwargs):
    """Sample as follows:
        - For each frame, calculate the centroid.
        - For each point in the frame, calculate the average distance from the
          centroid.
        - For some number of subranges ("buckets") in in this time series along
          the y axis (i.e. subranges of average distance), take a random
          sampling from each subrange
    """



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
