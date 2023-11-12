#!/bin/bash

# Start the run once job.
echo "Docker container has been started"

declare -p | grep -Ev 'BASHOPTS|BASH_VERSINFO|EUID|PPID|SHELLOPTS|UID' > /container.env

wget https://raw.githubusercontent.com/hammad93/hurricane-tts/main/hurricane_tts.ipynb
ipython --TerminalIPythonApp.file_to_run=hurricane-tts.ipynb