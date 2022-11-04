#!/usr/bin/env python3
"""
Normalisation.
"""
import os

import oepr.math
import oepr.util


@oepr.util.check_path('f')
def normalise(path_csv, path_out):
    df = oepr.util.csv_to_dataframe(path_csv)
    pc, pc_normalised, centroid, length = oepr.math.normalise_point_cloud(df)
    if (pc_normalised.min().min() >= -1 and pc_normalised.max().max() <= 1):
        pc_normalised.to_csv(path_out, index=False)
        print('normalised %s to %s' % (path_csv, path_out))


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
