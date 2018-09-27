#!/bin/bash

set -e
set -x

#Updates
sudo apt-get update
sudo apt-get install gcc-multilib g++-multilib wget unzip cmake

# Ninja
wget https://github.com/ninja-build/ninja/releases/download/v1.8.2/ninja-linux.zip
unzip ninja-linux.zip
sudo mv ninja /usr/bin/ninja
rm ninja-linux.zip

# Coverage
pip install codecov

pip install -r root-get-requirements/requirements.txt
