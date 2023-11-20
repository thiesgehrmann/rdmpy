# rdmpy
A small package to help mange file versioning and meta data.

It automatically generates user and timestamped files, together with a JSON file that stores additional metadata in the progeny of the data file.


# Installation
pip install https://github.com/thiesgehrmann/rdmpy


# Usage

```python

# Some data we want to write
import pandas as pd
D = pd.DataFrame([[1,2,3],[4,5,6],[7,8,9]], columns=['a','b','c'])

# Write it within a with clause
with RDM('my_new_file.txt','rw') as ofd:
    D.to_csv(ofd, index=False)
#ewith


# If we want to open the most recent file, we can do that by explicitly setting the read flag.
with RDM('my_new_file.txt', 'r') as ifd:
    X = pd.read_csv(ifd)
#ewith

```

## Specifying additional metadata

The real advantage of this approach is that we can store additional metadata in the json file.

```python
with RDM('my_new_file.txt','rw', source="~/repos/mymethod.ipynb", 'generated_for'='ColleagueX') as ofd:
    D.to_csv(ofd, index=False)
#ewith
```

## A note on modes

We define three modes: `r`, `w` and `rw`. `r` and `rw` are functionally equivalent. They selec the most recent file. Since we don't know what will happen with the file once the filename is provided, it always adds a mention in the JSON file of 'modified', though this doesn't mean the file will be modified. In order to not change the modified timestamp, set the parameter `modified=False`, and then this value will not be changed.

