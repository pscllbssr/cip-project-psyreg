# CIP Project

This repo is holding code for the CIP-project in FS23 at HSLU.

## Setup

The following code should be fine to get you up and running. Creates a virtual environment (venv) and installs the specified libraries from `requirements.txt`.

```bash
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

```

## Scrape Data

1. run `scraper_psyreg.py` to get the list of all available entries in the database
2. run `scraper_psyreg_details.py` to scrape the details of psychologists

## Analysis

to be done
