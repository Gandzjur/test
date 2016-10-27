#!/usr/bin/env sh

if [ $# -eq 0 ]; then
	echo "Usage:\n $0 <timestamp>"
	exit 1
fi
timestamp=$(date +%s)
diff=$(($timestamp - $1))
if [ "$diff" -lt 0 ]; then
	diff=$((0 - $diff))
fi
diff_in_hours=$(($diff/3600))
echo $diff_in_hours
