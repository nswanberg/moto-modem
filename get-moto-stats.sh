#!/bin/bash

GETMOTOPID=$(launchctl list com.nateswanberg.get-moto-stats | grep -o '[[:digit:]]\{5\}')

if [ $GETMOTOPID ]
then
  echo "Killing $GETMOTOPID"
  kill -9 $PID
fi

source /Users/nate/.pyenv/versions/moto-modem/bin/activate
SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
python $SCRIPT_DIR/moto.py >> $HOME/Dropbox/Records/Tech/mb8611/mb8611.log

