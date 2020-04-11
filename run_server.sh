#!/usr/bin/env bash

CURRENT_DIRECTORY="$(dirname $(realpath "$0"))"
cd "$CURRENT_DIRECTORY"

while true; do
    date
    pipenv run python3 bot.py | tee "$CURRENT_DIRECTORY/bot.log"
done