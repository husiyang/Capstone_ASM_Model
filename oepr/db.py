#!/usr/bin/env python3
"""Database"""
import sqlite3

SCHEMA = """
CREATE DATABASE oepr;

CREATE TABLE Take (
    id                   INT NOT NULL,
    capture_frame_rate   UNSIGNED FLOAT(24),
    coord_space          VARCHAR(31),
    exported_frame_count UNSIGNED SMALLINT,
    export_frame_rate    UNSIGNED FLOAT(24),
    format_version       UNSIGNED FLOAT(24),
    length_units         VARCHAR(31),
    name                 VARCHAR(63),
    notes                VARCHAR(255),
    rotation_type        VARCHAR(31),
    total_frame_count    UNSIGNED SMALLINT,

    PRIMARY KEY (id)
)

CREATE TABLE Frame (
    number  INT NOT NULL,
    timestamp   INT NOT NULL,
    id_take INT NOT NULL,
)
"""

if __name__ == '__main__':
    pass


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
