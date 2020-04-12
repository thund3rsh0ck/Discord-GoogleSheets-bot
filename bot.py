'''This is a bot that integrations google sheets with discord API. This Version uses the very base of the Repo it's forked from, but diverges a lot to track and report turnip prices for Animal Crossing New Horizons (ACNH)'''
# Python Libraries
import time
import os
import sys
import datetime
import json

# Pipfile Libraries
import pygsheets
import requests
import discord
import yaml

from typing import Mapping, Any

from discord.ext import commands
from oauth2client.service_account import ServiceAccountCredentials

# importing credentials and other configs

app_dir = os.path.abspath(os.path.dirname(__file__))
discord_file = os.path.join(app_dir, "theconfig.yaml")
google_file = os.path.join(app_dir, "theconfig.yaml")

with open(discord_file, mode="r") as discordfile:
    discordCreds: Mapping[str, Any] = yaml.load(discordfile, Loader=yaml.FullLoader)
    token, prefix = discordCreds["token"], discordCreds["prefix"]

with open(google_file, mode="r") as sheetsfile:
    sheetsConfig: Mapping[str, Any] = yaml.load(sheetsfile, Loader=yaml.FullLoader)

gsClient = None  # google sheets client
gsWorksheet = None  # google sheets worksheet that corresponds to the table

# create bot
bot = commands.Bot(command_prefix=prefix, pm_help=None,
                        case_insensitive=False)

def sheets_authorize(): 
    """This authorizes google sheets and lets you access the spreadsheet"""
    global gsClient
    global gsWorksheet
    gsClient = pygsheets.authorize()  #  only works if your OAUTH credentials are stored in a file named 'client_secret.json' in this directory
    spreadsheet = gsClient.open_by_key(sheetsConfig["spreadsheetId"])
    gsWorksheet = spreadsheet.worksheet("title", sheetsConfig["sheetName"])

def has_admin_privilege():
    """Check that returns true if user has admin permissions"""
    async def predicate(ctx):
        return await (bot.is_owner(ctx.author) or \
               ctx.author.permissions_in(ctx.channel).administrator)
    return commands.check(predicate)

@bot.command()
@has_admin_privilege()
async def reboot(ctx):
    """Admins use this to reboot the bot"""
    await ctx.send("Rebooting!...")
    await bot.logout()
    sys.exit(0)


@bot.event
async def on_ready():
	os.system("echo Logged in as {0.user}".format(bot))


@bot.command()
async def price(ctx, price: int, timezone: str):
    """'!price {$} {timezone}' with both being a number"""
    theEpoch = time.time()
    username = ctx.author.name
    userdiscrim = ctx.author.discriminator
    user = username + "#" + userdiscrim
    await ctx.send("Logging {}, in this timezone: {}".format(price, timezone))
    os.system("echo Priced Logged. User: {}, Price: {}, timezone: {}, epochtime: {}".format(user, price, timezone, theEpoch))


@bot.event
async def on_command_error(ctx, error):

    if isinstance(error, commands.CommandNotFound):
        # get message text
        return await ctx.send("Unknown command. Type {}help for help.".format(prefix))
    elif isinstance(error, commands.CheckFailure):
        return await ctx.send("You are not allowed to run this command.")
    else:
        raise error


if __name__ == "__main__":
    sheets_authorize()
    bot.run(token, bot=True, reconnect=True)
