#!/bin/bash

# check update (require user authorization)
sudo apt-get update

# install package manager poetry
pip install poetry

# setup python
virtualenv -p python3 venv
source venv/bin/activate

# install python dependencies
poetry install

# install spaCy pipeline
python3 -m spacy download en_core_web_md

echo "Installation completed!"