#!/bin/zsh

CAMPUS="$1"
PART_OF_SERVICE="${@:2}"
DATE="$(date +"%m.%d")"
DATEFMT="$(date +"%u%H%M")"
# All of the below are service times
# (Day of Week).(Time of day in 24hr)
SERVICES="$(<<EOF
41855 42015 0700 PM
70810 70930 0815 AM
70940 71100 0945 AM
71110 71230 1115 AM
EOF
)"

echo "$SERVICES" | while read i; do
if [ "$DATEFMT" -ge "$(echo $i | cut -d' ' -f1)" -a "$DATEFMT" -le "$(echo $i | cut -d' ' -f2)" ]; then
    echo "$CAMPUS $PART_OF_SERVICE $DATE - $(echo "$i" | cut -d' ' -f3,4)"
    exit
  fi
done

date +"$CAMPUS $PART_OF_SERVICE Testing %m.%d - %H%M"
