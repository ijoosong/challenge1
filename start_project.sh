#!/bin/bash

dir=$(pwd)
python -m venv my_env
source $dir/my_env/bin/activate
pip install -r requirements.txt
python app.py
