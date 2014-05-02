#!/bin/sh

BASEDIR=`dirname $0`

cd "$BASEDIR"

/usr/bin/python "$BASEDIR/LedTalker.py" $1
