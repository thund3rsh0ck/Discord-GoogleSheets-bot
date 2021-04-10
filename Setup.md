# How to Set Up:

## Config Files for Discord and Google Sheets API

This goes over getting the files for Google Sheet and Discord, and setting up some other global variables to help with the program. Everything is needed unless specifically needed.

### Setting up Discord Stuff
1. Open config.py and make sure it's writeable. That will handle the Discord Configurations

2. Go to this link [https: // discordapp.com / developers / applications / me /] and add a bot. To get your Token go to the Bot Page and add a bot. The Token should be at the top of the page, click Copy near the Username. Client ID is found on the General Information page, at the top, under the name.

3. To get your bots invite link go here https://discordapi.com/permissions.html

4. Go to the link provided, and add the bot to the right server.

### up Google Sheets API

Google Developers Platform: https://developers.google.com/sheets/api

1. This project uses pygsheets for Google Sheets, so follow the steps on the website. This application uses Oauth for the project
 
2. Follow the guide: https://pygsheets.readthedocs.io/en/stable/authorization.html

3. When you have the OAuth file, put it in the project folder, and name it client_secret.json