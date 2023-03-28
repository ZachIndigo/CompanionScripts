#!/bin/zsh

CAMPUS="$1"
PART_OF_SERVICE="${*:2}"
TIME="$(date +"%H%M")"
DOW="$(date +"%u")"
DATE="$(date +"%m.%d")"
if [ "$DOW" -eq 4 -a "$TIME" -gt 1855 -a "$TIME" -lt 2015 ]; then
  echo "$CAMPUS $PART_OF_SERVICE $DATE - 0700 PM"
  exit
elif [ "$DOW" -eq 6 ]; then
  if [ "$TIME" -gt 1525 -a "$TIME" -lt 1645 ]; then
    echo "$CAMPUS $PART_OF_SERVICE $DATE - 0330 PM"
    exit
  elif [ "$TIME" -gt 1655 -a "$TIME" -lt 1715 ]; then
    echo "$CAMPUS $PART_OF_SERVICE $DATE - 0500 PM"
    exit
  fi
elif [ "$DOW" -eq 7 ]; then
  if [ "$TIME" -gt 655 -a "$TIME" -lt 810 ]; then
    echo "$CAMPUS $PART_OF_SERVICE $DATE - 0700 AM"
    exit
  elif [ "$TIME" -gt 810 -a "$TIME" -lt 930 ]; then
    echo "$CAMPUS $PART_OF_SERVICE $DATE - 0815 AM"
    exit
  elif [ "$TIME" -gt 940 -a "$TIME" -lt 1100 ]; then
    echo "$CAMPUS $PART_OF_SERVICE $DATE - 0945 AM"
    exit
  elif [ "$TIME" -gt 1110 -a "$TIME" -lt 1230 ]; then
    echo "$CAMPUS $PART_OF_SERVICE $DATE - 1115 AM"
    exit
  fi
fi
date +"$CAMPUS $PART_OF_SERVICE Testing %m.%d - %H%M"
