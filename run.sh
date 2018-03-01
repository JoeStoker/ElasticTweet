#!/bin/bash

echo "Activating virtual environment"
. flask/bin/activate

echo "Running application"
FLASK_APP=view.py flask run
