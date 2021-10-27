#!/bin/bash

. /var/lib/vacation-planner/.nvm/nvm.sh
nvm use 12
while true; do
    npm start
    sleep 5
done
