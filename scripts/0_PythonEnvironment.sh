#!/bin/bash
set -e

# 
# Script to setup local python environment for RDFLIME.
# Flags:
#   --lbzip2    Install lbzip2, a faster decompression tool for our DBpedia data
#

scriptsRoot=$(dirname "${BASH_SOURCE[0]}")
rdflimeUtil=$scriptsRoot/..

cd $rdflimeUtil

# Install Build Tools for pyRDF2Vec dependencies and other prerequisites
sudo apt update
sudo apt install build-essential python3-dev git wget bzip2 python3-venv -y

# Allow for faster extraction
if [[ $* == *--lbzip2* ]]
then
    sudo apt install lbzip2 -y
    echo 'alias bzip2="lbzip2"' >> ~/.bashrc
    alias bzip2="lbzip2"
fi

# Get RDFLIME core implementation
git -C .. clone https://github.com/rgrenz/rdflime-core

# Get Poetry
curl -sSL https://install.python-poetry.org | python3 -
echo 'export PATH="~/.local/bin:$PATH"' >> ~/.bashrc
export PATH="~/.local/bin:$PATH"

# Install for util notebooks
poetry install 

# Install for core editing
# cd ../rdflime-core
# poetry run pip install -e .
