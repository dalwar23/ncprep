#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

# Import python libraries
import os
import sys
import argparse
import pandas as pd
try:
    from pyrainbowterm import *
except ImportError:
    print('Can not import pyrainbowterm!', log_type='error')
    print('Try: pip install pyrainbowterm', log_type='hint')
    sys.exit(1)
# Import file_operations
import _operations

# Source code meta data
__author__ = 'Dalwar Hossain'
__email__ = 'dalwar.hossain@protonmail.com'


# Clip data frame
def clip_data_frame(data_frame=None, start_date=None, periods=None):
    """
    This function clips (slices) pandas data frame according to dates and interval
    :param data_frame: Python pandas data frame
    :param start_date: start date of clipping
    :param periods: how many day's data to clip
    :return: Python pandas data frame
    """
    # Create a new column named 'date' and convert timestamps to human readable dates
    print('Converting unix timestamp into human readable dates.....', log_type='info')
    data_frame['date'] = pd.to_datetime(data_frame['timestamp'], unit='s', infer_datetime_format=True).dt.normalize()

    # Set the index of data frame at 'date' column
    print('Resetting data frame index.....', log_type='info')
    data_frame = data_frame.set_index('date')

    # Generate start date and end date for clipping from the input
    print('Generating text clipping date range.....', log_type='info')
    date_range = pd.date_range(start_date, periods=int(periods), freq='D')

    # Start date
    start_date = date_range[0]

    # End date
    end_date = date_range[-1]

    # Clip the data in between start date and end date
    print('Clipping desired data from data frame.....', log_type='info')
    data_frame = data_frame.loc[start_date:end_date]
    print('Desired data clipped successfully!', log_type='info', color='green')

    # Return
    return data_frame


# Load input file
def load_file(input_file=None, delimiter=None):
    """
    This function loads the input file into a python pandas data frame
    :param input_file: Input file path
    :param delimiter: column separator
    :return: Python pandas data frame
    """
    # Check delimiter
    if delimiter is None:
        delimiter = ' '
    else:
        delimiter = delimiter

    # Load input file
    print('Loading input dataset.....', log_type='info')
    # As the input file is being clipped, by default it should have 4 headers
    headers = ['source', 'target', 'weight', 'timestamp']
    try:
        data_frame = pd.read_csv(input_file, delimiter=delimiter, names=headers, skipinitialspace=True,
                                 comment='#')
        print('Input dataset loaded successfully!', color='green', log_type='info')
    except Exception as e:
        print('Can not load input dataset. ERROR: {}'.format(e), color='red', log_type='error')
        sys.exit(1)

    # Return
    return data_frame


# Create text clipper function
def clip_text(input_file=None, delimiter=None, start_date=None, interval=None):
    """
    This function controls the other functions
    :param input_file: Input file to clip
    :param delimiter: Column separator for input file
    :param start_date: Start date of clipping (dd-mm-YYYY)
    :param interval: for how many days (int)
    :return: clipped text, rest of the text
    """
    # Check sanity of the input file
    sanity_status = _operations.sanity_check(input_file=input_file, delimiter=delimiter)

    # If sanity check is passed, read and clip the text
    if sanity_status == 1:
        # Load input file
        data_frame = load_file(input_file=input_file, delimiter=delimiter)

        # Clip data frame
        clipped_text = clip_data_frame(data_frame=data_frame, start_date=start_date, periods=interval)

        # Create output file of the clipped data
        file_name, ext = input_file.rsplit('.', 1)
        output_file = file_name + '_clipped.' + ext
        _operations.create_output_file(data_frame=clipped_text, output_file_name=output_file)
    else:
        print('Sanity check failed!', log_type='error', color='red')
        sys.exit(1)


# Create command center
def command_center(input_file=None, delimiter=None, start_date=None, interval=None):
    """
    This function controls the other functions
    :param input_file: Input file to clip
    :param delimiter: Column separator for input file
    :param start_date: Start date of clipping (dd-mm-YYYY)
    :param interval: for how many days (int)
    :return: <>
    """
    print('Initializing.....', color='green', log_type='info')
    # Clip text according to input
    clip_text(input_file, delimiter, start_date, interval)
    pass


# Standard boilerplate for running this source code file as a standalone segment
if __name__ == '__main__':
    """
    Parse arguments and follow through to mission control
    """
    # Print initial message
    message = 'This script uses linux timestamps. Input file format => (source target weight timestamp)'
    _operations.initial_message(os.path.basename(__file__), custom_message=message)

    # Create parser
    parser = argparse.ArgumentParser(add_help=True)

    parser.add_argument('-i', '--input-file', action='store', dest='input_file', required=True,
                        help='Input file absolute path. E.g. /home/user/data/input/file_name.txt')
    parser.add_argument('-d', '--delimiter', action='store', dest='delimiter', required=False,
                        help='Separator for the input and output file. E.g. (,)/(";" need to be quoted)/tab/space. '
                             'Default (whitespace)')
    parser.add_argument('-s', '--from-date', action='store', dest='start_date', required=True,
                        help='Start date for clipping the file (dd-mm-YYYY)')
    parser.add_argument('-e', '--interval', action='store', dest='interval', required=True,
                        help='End interval. (int) e.g. 15 days from start date')

    # Parse arguments
    args = parser.parse_args()

    # Double checking the arguments
    if args.delimiter:
        _delimiter = args.delimiter
    else:
        print('No delimiter provided! Using default (whitespace).....', log_type='info')
        _delimiter = None
    if args.start_date:
        _start_date = args.start_date
        if len(_start_date.split('-')[0]) == 4:
            _start_date_ = _start_date
        else:
            print('Wrong date format! Try: (yyyy-mm-dd)', log_type='error', color='red')
            sys.exit(1)

    command_center(input_file=args.input_file, delimiter=_delimiter, start_date=_start_date_, interval=args.interval)
