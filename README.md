# rdmpy
A small package to help mange file versioning and meta data.

It automatically generates user and timestamped files, together with a JSON file that stores additional metadata in the progeny of the data file.


# Installation
pip install git+https://github.com/thiesgehrmann/rdmpy


# Usage

The usage is very simple and works in a `with` container block.

```python

# Some data we want to write
import pandas as pd
D = pd.DataFrame([[1,2,3],[4,5,6],[7,8,9]], columns=['a','b','c'])

# Write it within a with clause
with RDM('my_new_file.txt') as ofd:
    D.to_csv(ofd, index=False)
#ewith

# If we want to open the most recent file, we can do that by explicitly setting the read mode `mode='r'.
with RDM('my_new_file.txt', 'r') as ifd:
    X = pd.read_csv(ifd)
#ewith

# If we want to update the most recent file, we can do that by explicitly setting the read-write mode `mode=rw`.
with RDM('my_new_file.txt', 'rw') as ofd:
    D.to_csv(ofd, index=False)
#ewith

# If you need a file descriptor instead of a filename, you can get that with the `file=True` parameter:
with RDM('my_new_file.txt', 'rw', file=True) as ofd:
    ofd.write(str(X))
#ewith

# If we want to know the actual filepath that is generated, use the `tell=True` parameter:
with RDM('my_new_file.txt', 'rw', tell=True) as ofd:
    D.to_csv(ofd, index=False)
#ewith

```


## Specifying additional metadata

The real advantage of this approach is that we can store additional metadata in the JSON file that can't be stored in the filename itself.

```python
with RDM('my_new_file.txt',
         source="~/repos/mymethod.ipynb",
         generated_for='ColleagueX',
         description="A small table with data.") as ofd:
    D.to_csv(ofd, index=False)
#ewith
```

## A note on modes

We define three modes: `r`, `w` and `rw`. `r` and `rw` are functionally equivalent. They selec the most recent file. Since we don't know what will happen with the file once the filename is provided, it always adds a mention in the JSON file of 'modified', though this doesn't mean the file will be modified. In order to not change the modified timestamp, set the parameter `modified=False`, and then this value will not be changed.

