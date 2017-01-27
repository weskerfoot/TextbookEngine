#! /usr/bin/bash

virtualenv -p $(which python3) ./venv
source ./venv/bin/activate
pip3 install -r requirements.txt
deactivate
