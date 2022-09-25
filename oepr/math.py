#!/usr/bin/env python3
"""Mathematics/statistics"""


def get_centroid(points, n=3):
    """
    Get the centroid of an array of n-dimensional vectors
    We pass in n and do not check that the length of all the vectors is equal
    to n for efficiency's sake.
    """
    sums = (
        sum(p[d] for p in points) for d in range(n)
    )

    return [s / len(points) for s in sums]


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
