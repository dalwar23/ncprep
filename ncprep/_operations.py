#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

# Import python libraries
import os
import sys
import datetime
from itertools import islice
try:
    from pyrainbowterm import *
except ImportError:
    print('Can not import pyrainbowterm!', log_type='error')
    print('Try: pip install pyrainbowterm', log_type='hint')
    sys.exit(1)

# Source code meta data
__author__ = 'Dalwar Hossain'
__email__ = 'dalwar.hossain@protonmail.com'


# Get directory path for input/output data
def get_output_file(input_file):
    """
    This function extracts the directory path of input file and creates a new file name for the output file
    :param input_file: A complete file path for input dataset
    :return: A full path for output file
    """
    # Create output file name from input file in the same directory
    ext = '.txt'
    output_file_name = input_file.rsplit('.', 1)[0] + '_numeric' + ext

    # Return output path
    return output_file_name


# Create output file
def create_output_file(data_frame, output_file_name):
    """
    This function creates a file from python pandas data frame
    :param data_frame: Python pandas data frame
    :param output_file_name: Output file's full path with extension
    :return: NULL
    """
    # Create numeric output file
    print('Creating output file.....', log_type='info')
    try:
        data_frame.to_csv(output_file_name, index=False, header=False, sep=' ')
        print('Output file creation complete!', color='green', log_type='info')
    except Exception as e:
        print('Can not write output file. ERROR: {}'.format(e), log_type='error')
        sys.exit(1)


# Create headers based on weighted or unweighted
def generate_headers(weighted=None):
    """
    This function generates pandas header/names based on weighted or not parameter
    :param weighted: Boolean yes/no
    :return: headers, a python list
    """
    # Assign headers based on weighted or not
    if weighted == "yes" or weighted == "Yes" or weighted == "Y" or weighted == "y":
        headers = ['source', 'target', 'weight']
    elif weighted == "no" or weighted == "No" or weighted == "N" or weighted == "n":
        headers = ['source', 'target']
    else:
        print('Please provide weighted argument with yes/no, y/n, Yes/No', log_type='error')
        sys.exit(1)

    # Return
    return headers


# Check if the file has header or not
def file_sniffer(input_file=None):
    """
    This function checks if the first line of the file is a header or not
    :param input_file: Input file path
    :return: detected delimiter, headers (if available), number of columns, skip rows
    """
    try:
        import csv
    except ImportError:
        print('Can not import python csv library!', log_type='error')
        sys.exit(1)

    # Open the file and take a sniff
    with open(input_file) as f:
        first_five_lines = list(islice(f, 5))
        file_head = ''.join(map(str, first_five_lines))
        try:
            dialect = csv.Sniffer().sniff(file_head)
            _headers = csv.Sniffer().has_header(file_head)
            delimiter = dialect.delimiter
        except Exception as e:
            print('Can not detect delimiter or headers! ERROR: {}'.format(e), log_type='error')
            print('Please check input file!!', log_type='error')
        # Sniff into the file and see if there is a header or not
        if _headers:
            headers = file_head.split('\n')[0].split(delimiter)
            n_cols = len(headers)
            skip_rows = 1
        else:
            headers = None
            n_cols = len(file_head.split('\n')[0].split(delimiter))
            skip_rows = 0

    # Return
    return delimiter, headers, n_cols, skip_rows


# Check input file permissions
def check_input_file_permissions(input_file):
    """
    This function check permissions for the input file
    :param input_file: Input file path
    :return: input file, status of the file (OK/NOT OK) for reading
    """
    # Check input file's status (is a file?, has right permissions?)
    print('Checking input file status.....', log_type='info')
    if os.access(input_file, os.F_OK):
        print('Input file found!', log_type='info')
        if os.access(input_file, os.R_OK):
            print('Input file has read permission!', log_type='info')
            permission_status = 1
        else:
            print('Input file does not has read permission!', log_type='error')
            permission_status = 0
    else:
        print('Input file not found!', log_type='error')
        permission_status = 0

    # Return
    return input_file, permission_status


# Check File Header
def check_file_header(headers=None):
    """
    This file checks if the file header is active or commented
    Limitation: Checks only First line of the file
    :param headers: File headers with column names
    :return: 0/1 as header status code
    """
    if headers:
        if headers[0].startswith('#'):
            print('Found commented header!', log_type='info')
            header_status = 1
        else:
            header_status = 0
            print('Active headers detected! ', log_type='error', color='red', end='')
            print('Please comment [#] or delete header!', color='red')
            sys.exit(1)
    else:
        print('No headers detected!', log_type='info')
        header_status = 1

    # Return header status
    return header_status


# Check column indexes
def check_column_indexes(column_indexes):
    """
    This function checks column indexes
    :param column_indexes: Index of columns to be filtered
    :return: columns to use and column index status (yes/no)(1/0)
    """
    # Check column indexes (is numeric?)
    print('Checking column indexes.....', log_type='info')
    try:
        columns_to_use = column_indexes.split(',')
    except Exception as e:
        print('-c/--columns argument does not match input criteria! ERROR: {}'.format(e), log_type='error')
        print('Try: -c 1,4,6,3 or --columns 1,4,6,3 [Index starts from 1, separated by comma (,)]', log_type='hint')
    # Check if columns are in the list or not
    if columns_to_use:
        column_index_status = 1
    else:
        column_index_status = 0

    # Return
    return columns_to_use, column_index_status


# Check delimiter value
def check_delimiter_status(detected_delimiter=None, provided_delimiter=None):
    """
    This function check the delimiter
    :param detected_delimiter: delimiter detected by this program
    :param provided_delimiter: column separator
    :return: delimiter, delimiter status
    """
    print('Checking delimiter.....', log_type='info')

    print('Provided delimiter: "{}"'.format(provided_delimiter), log_type='info')
    print('Detected delimiter: "{}"'.format(detected_delimiter), log_type='info')

    if detected_delimiter != provided_delimiter:
        delimiter_status = 2
        print('Delimiter mismatch!', log_type='warn', color='orange')
    elif detected_delimiter == provided_delimiter:
        delimiter_status = 1

    # Return
    return provided_delimiter, delimiter_status


# Check output file's permission
def check_output_file_permissions(output_file):
    """
    This function check output file's permission and if exists, removes it
    :param output_file: output file path
    :return: output file, output file status
    """
    # Check output file
    print('Checking output file.....', log_type='info')
    if os.access(output_file, os.F_OK):
        try:
            print("Output file already exists! Removing old file.....", log_type='warn', color='orange')
            os.remove(output_file)
            output_file_status = 1
        except Exception as e:
            print('Can not remove previous file at output location! ERROR: {}'.format(e), log_type='error')
            output_file_status = 0
    else:
        print('Output file does not exists yet! It will be created!', log_type='hint')
        output_file_status = 1

    # Return
    return output_file, output_file_status


# Generate appropriate sanity check status code
def generate_sanity_status(input_file_status=None, column_indexes_status=None, header_status=None,
                           delimiter_status=None, output_file_status=None):
    """
    This function generates appropriate status code
    :param input_file_status: Permission status on the input file
    :param column_indexes_status: Columns to use status
    :param header_status: If the headers are present or not, or commented
    :param delimiter_status: Delimiter status for the input/output file
    :param output_file_status: Output file permission and status
    :return: status code (int)
    """
    status_code = 1
    print('Sanity check.....', log_type='info', end='')
    print('COMPLETE', color='green')
    print('--------------- Summary -------------------')

    # Input file
    if input_file_status:
        print('Input file.....', log_type='info', end='')
        if input_file_status == 1:
            print('OK', color='green')
            status_code = status_code and 1
        elif input_file_status == 0:
            print('NOT OK', color='red')
            status_code = status_code and 0

    # Columns to use
    if column_indexes_status:
        print('Columns.....', log_type='info', end='')
        if column_indexes_status == 1:
            print('OK', color='green')
            status_code = status_code and 1
        elif column_indexes_status == 0:
            print('NOT OK', color='red')
            status_code = status_code and 0

    # Headers
    if header_status:
        print('Headers.....', log_type='info', end='')
        if header_status == 1:
            print('OK', color='green')
            status_code = status_code and 1
        elif header_status == 0:
            print('NOT OK', color='red')
            status_code = status_code and 0

    # Delimiter
    if delimiter_status:
        print('Delimiter.....', log_type='info', end='')
        if delimiter_status == 1:
            print('OK', color='green')
            status_code = status_code and 1
        elif delimiter_status == 2:
            print('OK [!]', color='orange')
            print('Program might not work as expected if the file does not have default [whitespace] delimiter',
                  log_type='warn', color='orange')
            status_code = status_code and 1

    # Output file
    if output_file_status:
        print('Output file.....', log_type='info', end='')
        if output_file_status == 1:
            print('OK', color='green')
            status_code = status_code and 1
        elif output_file_status == 0:
            print('NOT OK', color='red')
            status_code = status_code and 0

    print('-------------------------------------------')

    # Return
    return status_code


# Sanity check
def sanity_check(input_file=None, column_indexes=None, delimiter=None, output_file=None):
    """
    This function verifies input(s)
    :param input_file: A file path to raw data file
    :param column_indexes: Indexes of the columns that needs to be filtered out (index starts from 1)
    :param delimiter: Column separator in input/output file (default is ',' [comma])
    :param output_file: A file path where the output will be stored
    :return: input_file, python list of column(s), column_separator, output_file
    """
    if input_file:
        # Get file information (Header, delimiter, number of columns etc.)
        detected_delimiter, headers, n_cols, skip_n_rows = file_sniffer(input_file)
        # Check input file's status
        input_file, input_file_status = check_input_file_permissions(input_file)
    else:
        input_file_status = 0

    if column_indexes:
        # Check column indexes
        columns_to_use, column_indexes_status = check_column_indexes(column_indexes)
        header_status = None
    else:
        column_indexes_status = 0
        header_status = check_file_header(headers)

    # If both input file and delimiter is provided
    if input_file and delimiter:
        # Check delimiter
        delimiter, delimiter_status = check_delimiter_status(detected_delimiter, delimiter)
    else:
        delimiter_status = 0

    # If input file is provided and delimiter
    if input_file and delimiter is None:
        # Check delimiter
        delimiter, delimiter_status = check_delimiter_status(detected_delimiter, delimiter)
    else:
        delimiter_status = 0

    if output_file:
        # Check output file
        output_file, output_file_status = check_output_file_permissions(output_file)
    else:
        output_file_status = 0

    sanity_status = generate_sanity_status(input_file_status, column_indexes_status, header_status, delimiter_status,
                                           output_file_status)

    # Return checked values
    return sanity_status


# Create initial message
def initial_message(script=None, custom_message=None):
    """
    This function creates initial message and prints it
    """
    marker = '-'  # Must be single character
    # Print a general help message
    date_time = datetime.datetime.now()
    _print_string = "Column based text filtering and processing"
    _print_string += " [ " + date_time.strftime("%d-%B-%Y %H:%M:%S") + " ]"
    # Help message display
    _help_string = "Need help?: python {} -h/--help".format(script)
    # Create prefix and suffix
    prefix = marker * 2 + ' '
    suffix = ' ' + marker * 2
    print_string = prefix + _print_string
    custom_message = prefix + custom_message
    help_string = prefix + _help_string
    # Take max
    str_length = max([len(print_string), len(custom_message), len(help_string)]) + 3
    # Create padding
    print_string = print_string + " " * (str_length - len(print_string) - len(suffix)) + suffix
    custom_message = custom_message + " " * (str_length - len(custom_message) - len(suffix)) + suffix
    help_string = help_string + " " * (str_length - len(help_string) - len(suffix)) + suffix
    # Print
    line_block = marker * str_length
    print(line_block, print_string, custom_message, help_string, line_block, sep='\n')
