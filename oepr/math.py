#!/usr/bin/env python3
"""Mathematics/statistics"""
import itertools

import numpy as np
import pandas as pd


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


def compute_pointcloud_centroid(pointcloud):
    """compute the centre point of 89 * 100 points"""
    centroid = []

    x, y, z = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    for i in range(0, 265, 3):
        new_x = pd.DataFrame(pointcloud.iloc[:,i].values)
        x = x.append(new_x, ignore_index=True)

    centroid.append(x.sum() / len(x))

    for j in range(1, 266, 3):
        new_y = pd.DataFrame(pointcloud.iloc[:,j].values)
        y = y.append(new_y, ignore_index=True)

    centroid.append(y.sum() / len(y))

    for k in range(2, 267, 3):
        new_z = pd.DataFrame(pointcloud.iloc[:,k].values)
        z = z.append(new_z, ignore_index=True)

    centroid.append(z.sum() / len(z))

    return pd.DataFrame(centroid)


def normalise_point_cloud(pointcloud):
    """normalise point cloud"""
    centroid = compute_pointcloud_centroid(pointcloud)
    centroid = centroid.T
    centroid = centroid.values
    centroid = list(itertools.chain.from_iterable(centroid))

    # put centre of the point cloud to (0, 0, 0)
    for i in range(0, 265, 3):
        pointcloud.iloc[:,i] = pointcloud.iloc[:,i] - centroid[0]
    for j in range(1, 266, 3):
        pointcloud.iloc[:,j] = pointcloud.iloc[:,j] - centroid[1]
    for k in range(2, 267, 3):
        pointcloud.iloc[:,k] = pointcloud.iloc[:,k] - centroid[2]

    # find the longest axis in XYZ axis and compute the length. This step
    # can get a scaling ratio.

    # Step 1: The point cloud after translation is squared
    # Step 2: Sum according to row. This step can get a 100*1 matrix. The
    # original matrix is 100*267
    # Step 3: Find the square root and find the maxiumn value as scaling
    # ratio
    m = np.max(np.sqrt(np.sum(pointcloud ** 2, axis=1)))

    # Scaling point cloud according the ratio
    # normalize point cloud to (-1,1) according to long axis
    pointcloud_normalized = pointcloud / m

    # centroid: center point, m: length of long axis, centroid and m can be
    # used to compute keypoints
    return pointcloud, pointcloud_normalized, centroid, m


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
