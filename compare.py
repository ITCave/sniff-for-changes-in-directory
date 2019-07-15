# -*- coding: utf-8 -*-
# @Filename : compare.py
# @Date : 2019-07-15-13-44
# @Project: ITC-sniff-for-changes-in-directory
# @Author: Piotr Wołoszyn
# @Website: http://itcave.eu
# @Email: contact@itcave.eu
# @License: MIT
# @Copyright (C) 2019 ITGO Piotr Wołoszyn

import os
import pickle
import argparse
from _datetime import datetime


def compare(ds1_path, ds2_path):
    """
    Function that compares content of two pickled
    :param ds1_path: path string
    :param ds2_path: path string
    :return: void
    """

    ds1_path = str(ds1_path).lower()
    ds2_path = str(ds2_path).lower()

    # File where the comparision result will be stored
    logfile_name = 'diff' + datetime.now().strftime('%Y%m%d%H%M%S') + '.csv'
    log = open(logfile_name, 'w')
    log.write("TYPE; SNAPSHOT1; SNAPSHOT2; CONTEXT\n")

    ds1 = pickle.load(open(ds1_path, 'rb'))
    ds2 = pickle.load(open(ds2_path, 'rb'))

    # Loop over directory state stored in the first path
    for subdir, content in ds1.items():

        if subdir in ds2:

            for f, f_det in content['file_details'].items():

                if f in ds2[subdir]['file_details']:

                    ds1_time = datetime.fromtimestamp(ds1[subdir]['file_details'][f][0]).isoformat()
                    ds2_time = datetime.fromtimestamp(ds2[subdir]['file_details'][f][0]).isoformat()

                    # Check if modification date changed
                    if ds1_time != ds2_time:
                        log.write("DATE MODIFIED;"
                                  + str(ds1_time) + ";" + str(ds2_time) + ";" + str(os.path.join(subdir, f)) + "\n")
                else:
                    log.write("MISSING FILE;exists;missing;" + os.path.join(subdir, f) + "\n")

        else:
            log.write("MISSING FOLDER;exists;missing;" + subdir + "\n")

    # Loop over directory state stored in the second path and check for missing/existing files
    for subdir, content in ds2.items():

        if subdir in ds1:

            for f, f_det in content['file_details'].items():

                if f not in ds1[subdir]['file_details']:
                    log.write("MISSING FILE;missing;exists;" + os.path.join(subdir, f) + "\n")
        else:
            log.write("MISSING FOLDER;missing;exists;" + subdir + "\n")

    print("Differences stored in: " + logfile_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Directory comparator')
    parser.add_argument('snapshot1', help='Path to the first snapshot file (.pkl)')
    parser.add_argument('snapshot2', help='Path to the second snapshot file (.pkl)')

    args = parser.parse_args()
    compare(args.snapshot1, args.snapshot2)
