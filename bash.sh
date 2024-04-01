#!/bin/bash

#create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

#install requirements
pip install -r requirements.txt
