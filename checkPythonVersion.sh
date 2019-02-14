#!/bin/bash

MYVAR=`python -c 'import sys; print(sys.version_info[0])'`
if (( $MYVAR == 2 ))
    then
        echo "Using Python2"
        sed -i '/mypy/d' requirements.txt
fi

