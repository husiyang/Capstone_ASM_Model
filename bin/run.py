#!/usr/bin/env python3
"""
Full script to run everything locally.
"""
import os
import sys

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


def main():
    train, test = read_sample()

    import pdb; pdb.set_trace()

    return getattr(os, 'EX_OK', 0)

if __name__ == '__main__':
    sys.exit(main())
