#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This package cna filter text based on column indexes, it can also clip data
based on timestamp and interval and map string data to numeric data if the
file is formatted as  -> source target weight timestamp
This package is specially designed for using with another python package
called 'neochain' to detect community structures in blockchain network

To install: python setup.py install
To use: import ncprep as ncp
"""


# Source code meta data
__author__ = 'Dalwar Hossain'
__email__ = 'dalwar.hossain@protonmail.com'


# Handle imports
from ncp_txtfilter import filter_columns
from ncp_txtclipper import clip_text
from ncp_txtmapper import numeric_mapper


# Version
__version__ = 1.0
