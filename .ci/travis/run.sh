#!/bin/bash

set -e
set -x

if [[ "$(uname -s)" == 'Darwin' ]]; then
    if which pyenv > /dev/null; then
        eval "$(pyenv init -)"
    fi
    pyenv activate root-get
    # OSX py3 do not show output in more than 10min causing the build to fail
    nosetests --with-coverage tests.unit --verbosity=2
else
   nosetests --with-coverage tests.unit --verbosity=2 --processes=4 --process-timeout=1000
fi
