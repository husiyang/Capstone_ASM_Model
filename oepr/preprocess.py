#!/usr/bin/env python3
"""
Preprocessing
"""
import collections
import random
import math
import statistics

import oepr.math
import oepr.util
import oepr.read

DEFAULT_SAMPLE_SIZE = 100


def mean_distance_from_centroid(points):
    """return the mean distance of a sent of points from their centroid"""
    centroid = oepr.math.get_centroid(points)
    distances = (math.dist(centroid, p) for p in points)
    return getattr(statistics, 'fmean', statistics.mean)(distances)


def get_sorted_random_deque_from_range(max_range, count, min_range=0):
    random_indices = random.sample(range(min_range, max_range), k=count)
    random_indices = sorted(random_indices)
    return collections.deque(random_indices)


@oepr.util.check_path('f')
def sample_average_bucketed_centroid_distance(path_csv, size=DEFAULT_SAMPLE_SIZE, **kwargs):
    """Sample as follows:
        - For each frame, calculate the centroid.
        - For each point in the frame, calculate the distance from the
          centroid.
        - Average these distances.
        - For some number of subranges ("buckets") in in this time series along
          the y axis (i.e. subranges of average distance), take a random
          sampling from each subrange
    """
    buckets = kwargs.get('buckets', 10)
    frame_numbers = list()

    frame_distances = (
        (f['frame'], mean_distance_from_centroid(f['points']))
        for f in oepr.read.get_data_take(path_csv)
    )
    frame_distances = sorted(frame_distances, key=lambda d: d[1])

    samples_per_bucket = size // buckets
    bucket_size = len(frame_distances) // buckets

    assert bucket_size

    for b in range(buckets):
        random_indices = get_sorted_random_deque_from_range(bucket_size, samples_per_bucket)
        bucket = frame_distances[b * bucket_size:(b + 1) * bucket_size]

        frame_numbers += [
            bucket[i][0] for i in random_indices
        ]

    for d in oepr.read.get_data_take(path_csv):
        if d['frame'] in frame_numbers:
            yield d


@oepr.util.check_path('f')
def sample_random(path_csv, size=DEFAULT_SAMPLE_SIZE):
    count_frames = oepr.read.get_info_take(path_csv)[oepr.read.KEY_TOTAL_FRAMES]

    random_indices = get_sorted_random_deque_from_range(count_frames, size)
    current_index = random_indices.popleft()

    for d in oepr.read.get_data_take(path_csv):
        if d['frame'] == current_index:
            yield d
            try:
                current_index = random_indices.popleft()
            except IndexError:
                break

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
