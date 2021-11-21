#!/bin/bash

source /Users/nate/.pyenv/versions/moto-modem/bin/activate
SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
python $SCRIPT_DIR/moto.py >> $HOME/Dropbox/Records/Tech/mb8611/mb8611.log
