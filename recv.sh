#!/bin/bash

pipe=$1

# Get path to the current script
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

# If no pipe was specifed, use the default value
if [[ ! -n "$pipe" ]]; then
    pipe=/tmp/sublime_exterminal_pipe
fi

# If the pipe doesn't exist, create it
if [[ ! -a $pipe ]]; then
    mkfifo $pipe
else
    # If something is in the way of the pipe, 
    # delete it, then create the pipe
    if [[ ! -p $pipe ]]; then
        rm -f $pipe
        mkfifo $pipe
    fi
fi

echo
echo Now accepting commands...
echo

# Read lines from the pipe in an infinite loop until closed
while true; do
    if read line < $pipe; then
        echo Running command:
        echo $line
        echo
        
        $DIR/subrecv.sh "$line"
        
        echo
        echo Awaiting another command...
        echo
    fi
done

echo Reader exiting...