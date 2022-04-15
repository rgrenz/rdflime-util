#!/bin/bash -i
# Interactive mode to allow sourcing ~./bashrc during execution.
# Run with sudo bash -i 0_PythonEnvironment.sh

# 
# Script to setup local python environment for RDFLIME
#

sudo apt update -y

# Install Build Tools for pyRDF2Vec dependencies 
sudo apt install build-essential python3-dev git wget bzip2 -y

# Allow for faster extraction
# sudo apt install lbzip2 -y
# echo 'alias bzip2="lbzip2"' >> .bashrc 

# Get Poetry
sudo apt install python3-venv -y
curl -sSL https://install.python-poetry.org | python3 -
echo 'export PATH="~/.local/bin:$PATH"' >> .bashrc
source ~/.bashrc

# Get RDFLIME 
git clone https://github.com/rgrenz/lime
cd lime

# Install python dependencies
poetry install
poetry run python ./setup.py install