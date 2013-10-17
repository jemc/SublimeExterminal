#!/bin/bash

pipe=$1

if [[ ! -n "$pipe" ]]; then
    pipe=/tmp/sublpipe
fi

if [[ -a $pipe ]] && [[ ! -p $pipe ]]; then
    rm -f $pipe
fi
mkfifo $pipe

echo
echo Now accepting commands...
echo

while true
do
    if read line < $pipe; then
        echo Running command:
        echo $line
        echo
        bash -c "$line"
        
        echo
        echo Awaiting another command...
        echo
    fi
done

echo Reader exiting...