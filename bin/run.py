#!/usr/bin/env python3
"""
Full script to run everything locally.
"""
import itertools
import os
import sys

import numpy as np
import pandas as pd


BASE_DIRS = (
    os.path.join(os.sep, 'content', 'drive', 'MyDrive', 'CapstoneDataset'),
    os.path.join(os.sep, 'home', 'thomas', 'University', 'capstone',
                 'Capstone_ASM_Model', 'sample'),
)

SAMPLE_DIRS = (
    ('sampled_training', 'sampled_test'),
    (os.path.join('train', 'csv'), os.path.join('test', 'csv'))
)

def read_sample():
    """read samples into dataframes"""
    dir_sample_train = ''
    dir_sample_test = ''
    base_dir = ''

    for index, b in enumerate(BASE_DIRS):
        if os.path.isdir(b):
            base_dir = b
            dir_sample_train, dir_sample_test = SAMPLE_DIRS[index]
            break
    else:
        raise RuntimeError('no base directory')

    dir_sample = {
        'train': os.path.join(base_dir, dir_sample_train),
        'test': os.path.join(base_dir, dir_sample_test)
    }

    assert all(os.path.isdir(d) for d in dir_sample.values())

    sampled_file_number = list(range(1, 19))

    def get_df(type_, number):
        """get dataframe"""
        path = os.path.join(dir_sample[type_], '%d.csv' % number)
        print(path)
        return pd.read_csv(path)

    relevant_fns = [n for n in sampled_file_number if n != 14]
    train = [get_df('train', n) for n in relevant_fns]
    test = [get_df('test', n) for n in relevant_fns]

    return train, test


def normalise(sampled_train_data, sampled_test_data):
    """normalisation"""

    # Compute the center point of 89*100 points.
    def compute_centroid(pc):
        centroid = []

        x, y, z = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

        for i in range(0, 265, 3):
            newX = pd.DataFrame(pc.iloc[:,i].values)
            x = x.append(newX, ignore_index=True)

        centroid.append(x.sum() / len(x))

        for j in range(1, 266, 3):
            newY = pd.DataFrame(pc.iloc[:,j].values)
            y = y.append(newY, ignore_index=True)

        centroid.append(y.sum() / len(y))

        for k in range(2, 267, 3):
            newZ = pd.DataFrame(pc.iloc[:,k].values)
            z = z.append(newZ, ignore_index=True)

        centroid.append(z.sum() / len(z))

        return pd.DataFrame(centroid)

    def normalize_point_cloud(pc):
        centroid = compute_centroid(pc)
        centroid = centroid.T
        centroid = centroid.values
        centroid = list(itertools.chain.from_iterable(centroid))

        # put centre of the point cloud to (0, 0, 0)
        for i in range(0, 265, 3):
            pc.iloc[:,i] = pc.iloc[:,i] - centroid[0]
        for j in range(1, 266, 3):
            pc.iloc[:,j] = pc.iloc[:,j] - centroid[1]
        for k in range(2, 267, 3):
            pc.iloc[:,k] = pc.iloc[:,k] - centroid[2]

        # find the longest axis in XYZ axis and compute the length. This step
        # can get a scaling ratio.

        # Step 1: The point cloud after translation is squared
        # Step 2: Sum according to row. This step can get a 100*1 matrix. The
        # original matrix is 100*267
        # Step 3: Find the square root and find the maxiumn value as scaling
        # ratio
        m = np.max(np.sqrt(np.sum(pc ** 2, axis=1)))

        # Scaling point cloud according the ratio
        pc_normalized = pc / m  # normalize point cloud to (-1,1) according to long axis

        # centroid: center point, m: length of long axis, centroid and m can be used to compute keypoints
        return pc, pc_normalized, centroid, m

    # export normalization data to csv
    normalise_dir = os.path.join(os.sep, 'home', 'thomas', 'University',
                                 'capstone', 'Capstone_ASM_Model', 'normalise')

    def export(sampled_data, norm_dir):
        count = 1
        for data in sampled_data:
            print(count)
            pc, pc_normalized, centroid, length = normalize_point_cloud(data)
            if (pc_normalized.min().min() >= -1 and pc_normalized.max().max() <= 1):
                path = os.path.join(norm_dir, '%d.csv' % count)
                pc_normalized.to_csv(path, index=False)
                print('finish output')
                count += 1

    export(sampled_train_data, os.path.join(normalise_dir, 'train'))
    export(sampled_test_data, os.path.join(normalise_dir, 'test'))


def main():
    train, test = read_sample()
    normalise(train, test)

    return getattr(os, 'EX_OK', 0)

if __name__ == '__main__':
    sys.exit(main())
