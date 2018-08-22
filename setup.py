#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Setup script for ncprep
Install ncprep with
python setup.py install
"""

# Source code meta data
__author__ = 'Dalwar Hossain'
__email__ = 'dalwar.hossain@protonmail.com'

# Import python libraries
import sys
from setuptools import setup


# Check if enough parameter has been given to install or not
if sys.argv[-1] == 'setup.py':
    print("To install, run 'python setup.py install'")
    print()


# Check python version before installing
if sys.version_info[:2] < (2, 7):
    print("NCPrep requires Python 2.7 or later (%d.%d detected)." % sys.version_info[:2])
    sys.exit(-1)


# Read the README.md file for long description
def readme():
    with open('README.md') as f:
        return f.read()


# Standard boilerplate to run this script
if __name__ == "__main__":
    setup(
        name='ncprep',
        version='1.0',
        maintainer='Dalwar Hossain',
        maintainer_email='dalwar.hossain@protonmail.com',
        author='Dalwar Hossain',
        author_email='dalwar.hossain@protonmail.com',
        description='ncprep - A text preparation package for blockchain data',
        keywords=['Network', 'Blockchain', 'Filtering', 'Clipping'],
        long_description=readme(),
        license='MIT',
        platforms=['Linux', 'Mac OSX', 'Windows', 'Unix'],
        url='https://github.com/dharif23/ncprep',
        download_url='https://github.com/dharif23/ncprep',
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Topic :: Software Development :: Libraries :: Python Modules'],
        packages='ncprep',
        include_package_data=True,
        install_requires=['pip>=18.0',
                          'argparse>=1.2.1',
                          'numpy==1.14.5',
                          'pandas>=0.23.4',
                          'pyrainbowterm>=1.0',
                          'subprocess32>=3.5.2',
                          'setuptools>=40.1.0',
                          'six>=1.11.0',
                          'wheel>=0.31.1',
                          'python-dateutil>=2.7.3',
                          'pytz>=2018.5',
                          'wsgiref >= 0.1.2',
                          'memory-profiler>=0.52.0'],
        test_suite='nose.collector',
        tests_require=['nose>=1.3.7', 'nose-cover3>=0.1.0'],
        zip_safe=False
    )