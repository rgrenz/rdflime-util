#!/bin/bash

# 
# Script to setup local python environment for RDFLIME.
# Flags:
#   --lbzip2    Install lbzip2, a faster decompression tool for our DBpedia data
#   --get-core  Also clone and setup the core RDFLIME implementation

sudo apt update -y

# Install Build Tools for pyRDF2Vec dependencies 
sudo apt install build-essential python3-dev git wget bzip2 python3-venv -y

# Allow for faster extraction
if [[ $* == *--lbzip2* ]]
then
    sudo apt install lbzip2 -y
    echo 'alias bzip2="lbzip2"' >> ~/.bashrc
    alias bzip2="lbzip2"
fi

# Get Poetry
curl -sSL https://install.python-poetry.org | python3 -
echo 'export PATH="~/.local/bin:$PATH"' >> ~/.bashrc
export PATH="~/.local/bin:$PATH"

# Install python dependencies for util repository
rdflimeUtil=$(dirname $0)/..
cd $rdflimeUtil
poetry install

# Get RDFLIME core implementation
if [[ $* == *--get-core* ]]
then
    git -C .. clone https://github.com/rgrenz/rdflime-core
    
    # Install for util notebooks
    poetry add ../rdflime-core

    # Install for core editing
    # cd ../rdflime-core
    # poetry run pip install -e .
fi