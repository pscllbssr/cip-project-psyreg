#!/bin/bash

# this installs all the python bindings and packages
# make a virtualenv
python3 -m venv venv

# activate virtualenv
source venv/bin/activate

# make sure wheel is available
pip install wheel

# install requirements
pip install -r requirements.txt
