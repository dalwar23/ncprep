#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

# Import python libraries
import os
import sys
import argparse
import subprocess
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


# Create awk command
def create_command(input_file, columns_to_use, column_separator, output_file):
    """
    This function creates the linux command to filter the columns and creating the output file
    :param input_file: A valid file path to raw data file
    :param columns_to_use: Indexes of the columns that needs to be filtered out (index starts from 1)
    :param column_separator: Column separator in input/output file (default is ',' [comma])
    :param output_file: A valid file path where the output will be stored
    :return: A linux shell command
    """
    print('Creating text filter command.....', log_type='info')
    column_indexes = columns_to_use.split(',')
    prefix, command_segment = ('$', '')
    count = 1
    index_length = len(column_indexes)
    for item in column_indexes:
        if count < index_length:
            segment = prefix + item + '" "'
            command_segment += segment
            count += 1
        else:
            segment = prefix + item
            command_segment += segment
    if column_separator is None:
        delimiter = ''
    else:
        delimiter = ' -F "' + column_separator + '"'
    command = "awk" + delimiter + " '{print " + command_segment + "}' " + input_file + " > " + output_file

    print('Command creation complete!', log_type='info', color='green')

    # Return command
    return command


# Create output file with filtered data from input file
def create_output_file(command):
    """
    This function uses python subprocess module to read input file, filter with AWK and store data in a output file
    :param command: A linux AWK command
    :return: Data stored in output file
    """
    print('Reading input file.....', log_type='info')
    try:
        print('Creating output file.....', log_type='info')
        subprocess.check_output(command, shell=True, universal_newlines=True).strip()
        print('Output file creation complete!', log_type='info', color='green')
    except Exception as e:
        print('Output file creation error. ERROR: {}'.format(e), color='red', log_type='error')
        sys.exit(1)


# Create filter columns
def filter_columns(input_file=None, column_indexes=None, delimiter=None, output_file=None):
    """
    This function filters text input depending on columns and delimiter
    :param input_file: A file path to raw data file
    :param column_indexes: Indexes of the columns that needs to be filtered out (index starts from 1)
    :param delimiter: Column separator in input/output file (default is ' ' [whitespace])
    :param output_file: A file path where the output will be stored
    :return: File object
    """
    # Check inputs to avoid Exceptions
    if input_file and column_indexes:
        # Check delimiter parameter
        if delimiter is None:
            print('No delimiter provided! Using default [whitespace].....', log_type='info')
            delimiter = None
        else:
            delimiter = delimiter

        # Check the output file parameter
        if output_file is None:
            print('No output file provided! Using same directory as input file.....', log_type='warn', color='orange')
            file_name, ext = input_file.rsplit('.', 1)
            output_file = file_name + '_cols.txt'
        else:
            output_file = output_file

        # Check sanity of input
        sanity_status = _operations.sanity_check(input_file=input_file, column_indexes=column_indexes,
                                                 delimiter=delimiter, output_file=output_file)
    else:
        print('Invalid parameters! Check input!!', log_type='error', color='red')
        sys.exit(1)

    # Check if sanity check is Okay
    if sanity_status == 1:
        # Double checking the delimiter
        if delimiter is None:
            command_delimiter = ' '  # Using default delimiter
        else:
            command_delimiter = delimiter
        command = create_command(input_file, column_indexes, command_delimiter, output_file)
        if command:
            create_output_file(command)
        else:
            print('There was an error in command creation!', log_type='error')
            sys.exit(1)
    else:
        print('Sanity check failed!', log_type='error', color='red')
        sys.exit(1)


# Command Center
def command_center(input_file=None, column_indexes=None, delimiter=None, output_file=None):
    """
    This function controls rest of the functions
    :param input_file: A file path to raw data file
    :param column_indexes: Indexes of the columns that needs to be filtered out (index starts from 1)
    :param delimiter: Column separator in input/output file (default is ',' [comma])
    :param output_file: A file path where the output will be stored
    :return: NULL
    """
    print('Initializing.....', log_type='info')

    filter_columns(input_file, column_indexes, delimiter, output_file)


# Standard boilerplate for running this source code file as a standalone segment
if __name__ == "__main__":
    """
    Parse given arguments and follow through to mission control
    """
    # Print initial message
    _operations.initial_message(os.path.basename(__file__))

    # Create parser
    parser = argparse.ArgumentParser(add_help=True)

    parser.add_argument('-i', '--input-file', action='store', dest='input_file', required=True,
                        help='Input file absolute path. E.g. /home/user/data/input/file_name.txt/.csv/.dat etc.')
    parser.add_argument('-c', '--columns', action='store', dest='columns', required=True,
                        help='Index of the columns (comma separated, index starting from 1) E.g. 1,4,2,5.')
    parser.add_argument('-d', '--delimiter', action='store', dest='delimiter', required=False,
                        help='Separator for the input file. E.g. (,)/(";" need to be quoted)/tab/space.'
                             'Default is whitespace')
    parser.add_argument('-o', '--output-file', action='store', dest='output_file', required=True,
                        help='Output file absolute path. E.g. /home/user/data/output/file_name.txt/.csv/.dat etc.')

    # Parse arguments
    args = parser.parse_args()

    # Double checking the arguments
    if args.delimiter:
        _delimiter = args.delimiter
    else:
        print('No delimiter provided! Default delimiter [whitespace] will be used.....', log_type='info')
        _delimiter = None

    command_center(input_file=args.input_file, column_indexes=args.columns, delimiter=_delimiter,
                   output_file=args.output_file)
