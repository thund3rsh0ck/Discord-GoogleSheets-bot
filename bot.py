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
    discordCreds: Mapping[str, Any] = yaml.load(
        discordfile, Loader=yaml.FullLoader)
    token, prefix = discordCreds["token"], discordCreds["prefix"]

with open(google_file, mode="r") as sheetsfile:
    sheetsConfig: Mapping[str, Any] = yaml.load(
        sheetsfile, Loader=yaml.FullLoader)

gsClient = None  # google sheets client
gsSalesWorksheet = None  # google sheets worksheet that corresponds to the selling price table
gsPurchaseWorksheet = None # google sheet worksheet that corresponds to the purchasing price table

# create bot
bot = commands.Bot(command_prefix=prefix, pm_help=None,
                   case_insensitive=False)


def sheets_authorize():
    """This authorizes google sheets and lets you access the spreadsheet"""
    global gsClient
    global gsSalesWorksheet
    global gsPurchaseWorksheet
    # only works if your OAUTH credentials are stored in a file named
    # 'client_secret.json' in this directory
    gsClient = pygsheets.authorize()
    spreadsheet = gsClient.open_by_key(sheetsConfig["spreadsheetId"])
    gsSalesWorksheet = spreadsheet.worksheet("title", sheetsConfig["salesName"])
    gsPurchaseWorksheet = spreadsheet.worksheet("title", sheetsConfig["purchaseName"])


def sales_sheets_handling(user, price, timezone, theEpoch):
    """This function handles selling price data being added to the spreadsheet and pushing the spreadsheet"""
    the_stuff = [user, price, timezone, theEpoch]
    gsSalesWorksheet.link(syncToCloud=True)
    worksheetAllValues = gsSalesWorksheet.get_all_values()  # this gets all the cells in the Worksheet
    rowNumbs = len(worksheetAllValues) # this checks for all the elements in the list, since each row is a set of elements within the main list
    latestRowNumb  = rowNumbs +1 # this creates the next cell number available for usage.
    gsSalesWorksheet.update_row(latestRowNumb, the_stuff) # this puts the information provided by the user, in the right cell
    gsSalesWorksheet.add_rows(1) # This adds 1 more row, to make sure we dont run out of rows for information. 

def purchase_sheets_handling(user, price, timezone, theEpoch):
    """This function handles buying price data being added to the spreadsheet and pushing the spreadsheet"""
    the_stuff = [user, price, timezone, theEpoch]
    gsPurchaseWorksheet.link(syncToCloud=True)
    worksheetAllValues = gsPurchaseWorksheet.get_all_values()  # this gets all the cells in the Worksheet
    rowNumbs = len(worksheetAllValues) # this checks for all the elements in the list, since each row is a set of elements within the main list
    latestRowNumb  = rowNumbs +1 # this creates the next cell number available for usage.
    gsPurchaseWorksheet.update_row(latestRowNumb, the_stuff) # this puts the information provided by the user, in the right cell
    gsPurchaseWorksheet.add_rows(1) # This adds 1 more row, to make sure we dont run out of rows for information. 



def has_admin_privilege():
    """Check that returns true if user has admin permissions"""
    async def predicate(ctx):
        return await (bot.is_owner(ctx.author) or
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
async def sell_price(ctx, price: int, timezone: str):
    """'!price {$} {timezone}' with both being a number"""
    theEpoch = time.time()
    username = ctx.author.name
    userdiscrim = ctx.author.discriminator
    user = username + "#" + userdiscrim
    await ctx.send("Logging {}, in this timezone: {}".format(price, timezone))
    os.system(
        "echo Priced Logged. User: {}, Price: {}, timezone: {}, epochtime: {}".format(
            user,
            price,
            timezone,
            theEpoch))
    sales_sheets_handling(user, price, timezone, theEpoch)

@bot.command()
async def buy_price(ctx, price: int, timezone: str):
    """'!buy_price {$} {timezone}' with both being a number"""
    theEpoch = time.time()
    username = ctx.author.name
    userdiscrim = ctx.author.discriminator
    user = username + "#" + userdiscrim
    await ctx.send("Logging {}, in this timezone: {}".format(price, timezone))
    os.system(
        "echo Priced Logged. User: {}, Price: {}, timezone: {}, epochtime: {}".format(
            user,
            price,
            timezone,
            theEpoch))
    purchase_sheets_handling(user, price, timezone, theEpoch)



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
