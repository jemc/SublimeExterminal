#!/bin/bash

pipe=$1

if [[ ! -n "$pipe" ]]; then
    pipe=/tmp/sublpipe
fi

trap "rm -f $pipe" EXIT

if [[ ! -p $pipe ]]; then
    mkfifo $pipe
fi

echo
echo Now accepting commands...
echo

while true
do
    if read line <$pipe; then
        if [[ "$line" == 'quit' ]]; then
            break
        fi
        
        echo Running command:
        echo $line
        echo
        bash -c "$line"
        echo
        echo Awaiting another command...
        
    fi
done

echo "Reader exiting"