#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

# Import python libraries
import sys
import pandas as pd
import math
import datetime
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


# Numeric mapping of the entire data
def __numeric_mapping(data_frame, mapping_dict):
    """
    This function maps every string values into a numeric values in pandas data frame
    :param data_frame: Python pandas data frame
    :param mapping_dict: Python dictionary with str -> number(int/long) mapping
    :return: Python pandas data frame
    """
    # Map source and target row according to mapping dictionary
    print('Mapping data frame.....', log_type='info')
    data_frame['source'] = data_frame['source'].map(mapping_dict)
    data_frame['target'] = data_frame['target'].map(mapping_dict)

    # Return mapped data frame
    return data_frame


# Extract unique nodes/values for mapping
def __extract_nodes(data_frame):
    """
    This function extracts unique values from a python pandas data frame given that first two columns have headers
    'source' and 'target'
    :param data_frame: Python pandas data frame
    :return: Python dictionary with unique values mapped to an integer
    """
    # Find unique values to create a look up table
    # Returns a numpy array
    print('Extracting unique values/nodes.....', log_type='info')
    unique_values = pd.unique(data_frame[['source', 'target']].values.ravel('K'))

    # Create a PANDAS data frame out of numpy array with unique nodes
    print('Converting values into pandas data frame.....', log_type='info')
    lookup_data = pd.DataFrame(unique_values, columns=['label'])
    lookup_data['id'] = lookup_data.index
    print('Total detected nodes/values: ', log_type='info', end='')
    print('{}'.format(len(lookup_data.index)), color='cyan', text_format='bold')

    # Create a mapping dictionary for the node labels
    print('Creating mapping table.....', log_type='info')
    mapping_dict = dict(zip(lookup_data.label, lookup_data.id))

    # Return mapping dictionary
    return mapping_dict


# Clean and convert weights into normalized form (rounded up to 6 decimal point)
def __clean_convert_weight(x):
    """
    This function strips any white space and new lines. It also converts the value to a numpy 64 bit integer.
    Also normalizes big and small values using natural logarithm and rounding them up to 6 decimal points.
    :param x: Any number variable that can be converted into int/float/long/double
    :return: Natural logarithm of input value
    """
    x = x.replace(' ', '').replace('\n', '')
    x = int(x)
    log_x = round(math.log(1 + x), 2)
    return log_x


# Load input file in to pandas data frame
def __load_file(input_dataset, column_separator, headers):
    """
    This function reads a text file and loads it into python pandas data frame
    :param input_dataset: A file path that contains row x column wise text data
    :param column_separator: A value that separates the columns in the input dataset
    :param headers: Names of the columns from input dataset
    :return: Python pandas data frame
    """
    # Check headers
    if len(headers) == 3:
        convert_dict = {'weight': __clean_convert_weight}
        columns_to_use = [0, 1, 2]
    else:
        convert_dict = {}
        columns_to_use = [0, 1]

    # Check delimiter
    if column_separator is None:
        delimiter = ' '
    else:
        delimiter = column_separator

    # Load input file
    print('Loading input dataset.....', log_type='info')
    try:
        data_frame = pd.read_csv(input_dataset, delimiter=delimiter, names=headers, skipinitialspace=True,
                                 converters=convert_dict, comment='#', usecols=columns_to_use)
        print('Input dataset loading complete!', color='green', log_type='info')
    except Exception as e:
        print('Can not load input dataset. ERROR: {}'.format(e), color='red', log_type='error')
        sys.exit(1)

    # Drop rows that contains NaN/Blank column values
    print('Removing empty target/destination(s).....', log_type='info')
    data_frame = data_frame.dropna()

    # Filter out source and target column for values with valid length
    print('Cleaning data.....', log_type='info')
    data_frame = data_frame[~data_frame[['source', 'target']].applymap(lambda x: len(str(x)) < 34).any(axis=1)]

    # Reset index of the data frame
    print('Resetting data frame index.....', log_type='info')
    data_frame = data_frame.reset_index(drop=True)

    # Return pandas data frame
    return data_frame


# Create numeric mapping
def numeric_mapper(input_file=None, delimiter=None, weighted=None):
    """
    This function maps the strings to numeric values
    :param input_file: Input file path
    :param delimiter: Column separator
    :param weighted: yes/no if the file contains weights of the edges or not
    :return: file object
    """
    # Check the weighted arguments are provided
    if input_file and weighted:
        sanity_status = _operations.sanity_check(input_file=input_file)
    else:
        print('Invalid parameters! Check input!!', log_type='error', color='red')
        sys.exit(1)

    # If sanity check passed start string to numeric mapping
    if sanity_status == 1:
        headers = _operations.generate_headers(weighted)
        output_file_name = _operations.get_output_file(input_file)
        data_frame = __load_file(input_file, delimiter, headers)
        print('Data cleanup complete!', color='green', log_type='info')
        mapping_dict = __extract_nodes(data_frame)
        print('Numeric mapping reference creation complete!', color='green', log_type='info')
        start_time = datetime.datetime.now()
        print('Numeric mapping started at: {}'.format(start_time.strftime("%H:%M:%S")), log_type='info')
        numeric_data_frame = __numeric_mapping(data_frame, mapping_dict)
        mapping_end_time = datetime.datetime.now() - start_time
        print('Elapsed time for mapping: ', log_type='info', end='')
        print('{}'.format(mapping_end_time), color='cyan', text_format='bold')
        print('Numeric mapping complete!', color='green', log_type='info')

        _operations.create_output_file(numeric_data_frame, output_file_name)
    else:
        print('Sanity check failed!', log_type='error', color='red')
        sys.exit(1)
