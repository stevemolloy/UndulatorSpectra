python -m unittest discover -s tests/

MYVAR=`python -c 'import sys; print(sys.version_info[0])'`
if (( $MYVAR == 2 ))
	then
		echo "Using Python2"
		mypy --py2 tests
elif (( $MYVAR == 3 ))
	then
		echo "Using Python3"
		mypy tests
fi
