#!/usr/bin/env bash

# kills the bot and restarts it, restarting it forever
# if it fails

CURRENT_DIRECTORY="$(dirname $(realpath "$0"))"
cd "$CURRENT_DIRECTORY"

forever stopall

forever start --uid "plant-discord-bot" \
	--logFile "${CURRENT_DIRECTORY}/bot.log" \
	--append --spinSleepTime 5000  --minUptime 10000 \
	--sourceDir "$CURRENT_DIRECTORY" \
	-c "bash" "pipenv_wrapper.sh"

