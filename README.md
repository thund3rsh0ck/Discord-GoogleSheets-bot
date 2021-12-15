# Discord Sheets Bot Integration
This is a bot that integrations google sheets with discord API. It was intended to track participation for a game called CATS for Android but could be used for anything

# Requirements

1. Python 3.6
2. Discord.py from here: https://github.com/Rapptz/discord.py - install in the folder using python3 setup.py install
3. gspread from here: https://github.com/burnash/gspread - install in the folder using python3 setup.py install
4. oauth2client - `pip3 install --upgrade oauth2client`
5. If you get a error about pip3 above you may need to run something like `apt-get install -y python3-pip` on linux

# If You have Github Desktop use this
```
git clone https://github.com/thund3rsh0ck/Discord-GoogleSheets-bot
```
Then Open Up The File Named ReadMe.txt


# How To Set Up The Bot

1. Download The Zip File If you dont have Github Desktop
2. unzip.
3. Go To [Here](https://discordapp.com/developers/applications/me/) To Get Your Bot's Application ID, Token - you may need to go the documentation tab the the application tab as that site is a bit buggy. You will have to go under the "Bot" submenu and convert your bot to have life to get these values.
4. Next to get your Bots Invite link Go [Here](https://discordapi.com/permissions.html) and Get your Bots App ID and paste it into the "Client Id Here"
5. Select the Perms You want the bot to have and copy the invite link and paste it into the "link" in the "Config.py" File
6. Now Invite the bot to Your Server and Make a role Named "bot" (or whatever you want)
7. Get your google sheets json creds with this guide: https://gspread.readthedocs.io/en/latest/oauth2.html, plug that file into the bot.py as needed.
8. Now Double click the "bot.py" and The bot should work or run `python3 bot.py` on linux

# Issues

1. Open up an Issue

# Credits
Based off this bot from SamArroyos22: https://github.com/SamArroyos22/BasicDiscord-Bot
