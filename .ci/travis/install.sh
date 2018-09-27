#!/bin/bash

set -e
set -x

if [[ "$(uname -s)" == 'Darwin' ]]; then
    brew update || brew update
    brew outdated pyenv || brew upgrade pyenv
    brew install pyenv-virtualenv
    brew install pkg-config
    brew install ninja

    if which pyenv > /dev/null; then
        eval "$(pyenv init -)"
    fi
    if which pyenv > /dev/null; then
        eval "$(pyenv init -)"
    fi

    case "${PYVER}" in
        py27)
            pyenv install 2.7.10
            pyenv virtualenv 2.7.10 root-get
            ;;
        py33)
            pyenv install 3.3.6
            pyenv virtualenv 3.3.6 root-get
            ;;
        py34)
            pyenv install 3.4.3
            pyenv virtualenv 3.4.3 root-get
            ;;
        py35)
            pyenv install 3.5.0
            pyenv virtualenv 3.5.0 root-get
            ;;
        py36)
            pyenv install 3.6.0
            pyenv virtualenv 3.6.0 root-get
            ;;

    esac
    pyenv rehash
    pyenv activate root-get
else
   #Updates
   sudo apt-get update
   sudo apt-get install gcc-multilib g++-multilib wget unzip cmake

   # Ninja
   wget https://github.com/ninja-build/ninja/releases/download/v1.8.2/ninja-linux.zip
   unzip ninja-linux.zip
   sudo mv ninja /usr/bin/ninja
   rm ninja-linux.zip
fi

# Coverage
pip install codecov

pip install -r root-get-requirements/requirements.txt
