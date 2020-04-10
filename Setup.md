# How to Set Up:

## Config Files for Discord and Google Sheets API

This goes over getting the files for Google Sheet and Discord, and setting up some other global variables to help with the program. Everything is needed unless specifically needed.

### Setting up Discord Stuff
1. Open config.py and make sure it's writeable. That will handle the Discord Configurations

2. Go to this link [https://discordapp.com/developers/applications/me/] and add a bot. To get your Token go to the Bot Page and add a bot. The Token should be at the top of the page, click Copy near the Username. Client ID is found on the General Information page, at the top, under the name.

3. To get your bots invite link go here https://discordapi.com/permissions.html

4. Get the client ID from the Discord Config file, and enter it into the Client ID field. Select what permissions you want (For this bot, Read and Send messages are the two you'll need.)

## Setting up Google Sheets API

Google Developers Platform: https://developers.google.com/sheets/api

1. Go to the Python page for Google Sheets API (https://developers.google.com/sheets/api/quickstart/python)

2. Hit Enable Google Sheet API and select Desktop App. It should load for a couple seconds, and then display a couple strings, and give you the option to download a credential.json file. 

3. After the credential.json file has been downloaded, drag the file into this git folder, at the top of this directory.

Credits:
based off basic discord bot by Sam Arroyos: https://github.com/SamArroyos22/BasicDiscord-Bot