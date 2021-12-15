# Discord Sheets Bot Integration
This is a bot that integrations google sheets with discord API. It was intended to track participation for a game called CATS for Android but could be used for anything

# Requirements

1. Python 3.6
2. Discord.py from here: https://github.com/Rapptz/discord.py
3. gspread from here: https://github.com/burnash/gspread

# If You have Github Desktop use this
```
git clone https://github.com/thund3rsh0ck/Discord-GoogleSheets-bot
```
Then Open Up The File Named ReadMe.txt


# How To Set Up The Bot

1. Download The Zip File If you dont have Github Desktop
2. unzip.
3. Go To [Here](https://discordapp.com/developers/applications/me/) To Get Your Bots ID, Toke - you may need to go the documentation tab the the application tab as that site is a bit buggy.
4. Next to get your Bots Invite link Go [Here](https://discordapi.com/permissions.html) and Get your Bots id and paste it into the "Client Id Here"
5. Select the Perms You want the bot to have and copy the invite link and paste it into the "link" in the "Config.py" File
6. Now Invite the bot to Your Server and Make a role Named "bot" (or whatever you want)
7. Get your google sheets json creds with this guide: https://gspread.readthedocs.io/en/latest/oauth2.html, plug that file into the bot.py as needed.
8. Now Double click the "bot.py" and The bot should work

# Issues

1. Open up an Issue

# Credits
Based off this bot from SamArroyos22: https://github.com/SamArroyos22/BasicDiscord-Bot
