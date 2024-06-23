#!/bin/bash

HOURS=${HOURS:-12}

while true; do
/usr/src/app/write_vars.sh
/usr/src/app/run.sh

sleep $((HOURS * 60 * 60))
done
