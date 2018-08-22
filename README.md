# ncprep
A preparation package for NEOChain (Network Evolution Observation for Blockchain)

# Getting Started
```python
python setup.py install
```

# Description
This package filters text based on column indexes (column index starts from 1), clips data from file based on dates and
intervals and also maps string column values to numeric column values.

## Column based text filtering
```python
# Import the ncprep package
import ncprep as ncp

# Filter columns from a text file
ncp.filter_columns(input_file='path/to/input/file', column_indexes='1,2,3',
                   delimiter=',' , output_file='path/to/output/file')
```

This will create a file as `output_file` with `1,2,3` columns from `input_file`. 

:exclamation: parameter `output_file` \[*optional*\], if not provided, the program will create a `output_file` at the
same directory as `input_file` and the new file will have `_cols.txt` at the end of input file.

:exclamation: Parameter `delimiter` is \[*optional*\] if not provided, the program will consider `whitespace` as default
delimiter.


## Date and Interval based text clipping
```python
# Import the ncprep package
import ncprep as ncp

# Clip rows (text) from a text file based on UNIX timestamp
ncp.clip_text(input_file='/path/to/data/file', delimiter=',', start_date='2017-07-01', interval=15)

```
\[*whitespace*\] delimiter is expected, but can have other delimiters also.

This will create a file that contains all the rows from `2017-07-01` till next 15 days. The `output_file` will be
created at the same directory as input file with `_clipped.txt` at the end.

:fire: Input file format must match => (source target weight timestamp) (timestamp = UNIX timestamp)

:exclamation: Parameter `delimiter` is \[*optional*\] if not provided, the program will consider `whitespace` as default
delimiter.

# String to Numeric mapping
```python
# Import the ncprep package
import ncprep as ncp

ncp.numeric_mapper(input_file='/path/to/data/file', delimiter=',', weighted='yes')

```
\[*whitespace*\] delimiter is expected, but can have other delimiters also.

:fire: Input file format must match => (source target weight) or (source target)

:fire: Parameter weighted defines if the file is weighted or not, if weighted, returns natural logarithm of weight as
third column

:exclamation: Parameter `delimiter` is \[*optional*\] if not provided, the program will consider `whitespace` as default
delimiter.

# Notes
Don't forget to import the following at the beginning of the file
```python
from __future__ import print_function
```
