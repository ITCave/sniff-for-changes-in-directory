# -*- coding: utf-8 -*-
# @Filename : take_snapshot.py
# @Date : 2019-07-15-13-44
# @Project: ITC-sniff-for-changes-in-directory
# @Author: Piotr Wołoszyn
# @Website: http://itcave.eu
# @Email: contact@itcave.eu
# @License: MIT
# @Copyright (C) 2019 ITGO Piotr Wołoszyn


# Generic imports
import os
import pickle
import re
import argparse
from datetime import datetime


def clear_path_string(s):
    """
    Simple function that removes chars that are not allowed in file names
    :param s: path_string
    :return: cleaned_path_string
    """
    return (re.sub('[^a-zA-Z]+', '#', s)).lower()


def sniff(sniff_path):
    """
    Walks the path and stores information about directory content
    :param sniff_path: relative or absolute path
    :return: void
    """

    sniff_path = str(sniff_path).lower()

    # Variable in which information will be stored
    dir_store = {}

    # Recursive loop that walks through all of the subdirectories
    for subdir, dirs, files in os.walk(sniff_path):

        if subdir not in dir_store:
            dir_store[subdir] = {}

        dir_store[subdir]['subdirs'] = dirs
        dir_store[subdir]['files'] = files
        dir_store[subdir]['file_details'] = {}

        for file in files:

            f_path = os.path.join(subdir, file)

            # The information that will be store for each of the files - in this case last file modification date
            # Important: it's cross-platform relevant!
            modified_date = os.path.getmtime(f_path)
            dir_store[subdir]['file_details'][file] = (modified_date,)

    # Name of a file in which data will be stored
    dump_name = clear_path_string(sniff_path) + '_' + datetime.now().strftime('%Y%m%d%H%M%S')

    # Save pickled data
    with open(dump_name + '.pkl', 'wb') as output:
        pickle.dump(dir_store, output, pickle.HIGHEST_PROTOCOL)

    print("Directory Snapshot taken:", dump_name)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Directory Sniffer')
    parser.add_argument('path', help='Path to the directory that you want to take a snapshot of')
    args = parser.parse_args()
    sniff(args.path)
