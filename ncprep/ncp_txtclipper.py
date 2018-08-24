#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

# Import python libraries
import sys
import pandas as pd
from pyrainbowterm import *

# Import file_operations
import _operations


# Source code meta data
__author__ = 'Dalwar Hossain'
__email__ = 'dalwar.hossain@protonmail.com'


# Clip data frame
def __clip_data_frame(data_frame=None, start_date=None, periods=None):
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
    print('Clipping desired data.....', log_type='info')
    data_frame = data_frame.loc[start_date:end_date]
    print('Desired data clipping complete!', log_type='info')

    # Return
    return data_frame


# Load input file
def __load_file(input_file=None, delimiter=None):
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
        print('Input dataset loading complete!', log_type='info')
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
    # Check inputs to avoid exceptions
    if input_file and start_date and interval:
        # Check delimiter
        if delimiter is None:
            print('No delimiter provided! Using default [whitespace].....', log_type='info')
            delimiter = None  # No delimiter provided
        else:
            delimiter = delimiter

        # Check sanity of the input file
        sanity_status = _operations.sanity_check(input_file=input_file, delimiter=delimiter)

    else:
        print('Invalid parameters! Check input!!', log_type='error', color='red')
        sys.exit(1)

    # If sanity check is passed, read and clip the text
    if sanity_status == 1:
        # Load input file
        data_frame = __load_file(input_file=input_file, delimiter=delimiter)

        # Clip data frame
        clipped_text = __clip_data_frame(data_frame=data_frame, start_date=start_date, periods=interval)

        # Create output file of the clipped data
        file_name, ext = input_file.rsplit('.', 1)
        output_file = file_name + '_clipped.' + ext
        _operations.create_output_file(data_frame=clipped_text, output_file_name=output_file)
    else:
        print('Sanity check failed!', log_type='error', color='red')
        sys.exit(1)
