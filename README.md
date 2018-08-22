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
ncp.filter_columns(input_file='path/to/input/file', column_indexes='1,2,3', delimiter=','
, output_file='path/to/output/file')
```

This will create a file as `output_file` with `1,2,3` columns from `input_file`. 

:exclamation: parameter `delimiter` can be skipped if the `input_file` has \[whitespace\] as delimiter.

:exclamation: parameter `output_file` \[*optional*\], if not provided, the program will create a `output_file` at the
same directory as `input_file` and the new file will have `_cols.txt` at the end of input file.

# Note
Don't forget to import the following at the beginning of the file
```python
from __future__ import print_function
```
