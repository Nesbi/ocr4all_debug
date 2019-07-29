#!/bin/bash -e

DELTA=0
if [ $1 == "-d" ]
then
	echo "$(free -m | grep total | sed -E 's/^    (.*)/\1/g')  delta"
else
	echo "date     time $(free -m | grep total | sed -E 's/^    (.*)/\1/g')"
fi
while true; do
	if [ $1 == "-d" ]
	then
		echo "$(free -m | grep Mem: | sed 's/Mem://g') $DELTA"
	else
		echo "$(date '+%Y-%m-%d %H:%M:%S') $(free -m | grep Mem: | sed 's/Mem://g')"
	fi
	DELTA=$((DELTA+1))
	sleep 1
done
