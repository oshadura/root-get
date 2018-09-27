#!/bin/bash

set -e
set -x

nosetests --with-coverage tests.unit --verbosity=2 --processes=4 --process-timeout=1000
