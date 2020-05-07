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
import pandas as pd
import pytz

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
# google sheets worksheet that corresponds to the selling price table
gsSalesWorksheet = None
# google sheet worksheet that corresponds to the purchasing price table
gsPurchaseWorksheet = None
# google sheet that corresponds to discord users Pytz timezone data
gsUserTimezones = None
# google sheets that corresponds to error reporting.
gsNetworkErrors = None

# create bot
bot = commands.Bot(command_prefix=prefix, pm_help=None,
                   case_insensitive=False)


def sheets_authorize():
    """This authorizes google sheets and lets you access the spreadsheet"""
    global gsClient
    global gsSalesWorksheet
    global gsPurchaseWorksheet
    global gsUserTimezones
    global gsNetworkErrors
    # only works if your OAUTH credentials are stored in a file named
    # 'client_secret.json' in this directory
    gsClient = pygsheets.authorize()
    spreadsheet = gsClient.open_by_key(sheetsConfig["spreadsheetId"])
    gsSalesWorksheet = spreadsheet.worksheet(
        "title", sheetsConfig["salesName"])
    gsPurchaseWorksheet = spreadsheet.worksheet(
        "title", sheetsConfig["purchaseName"])
    gsUserTimezones = spreadsheet.worksheet("title", sheetsConfig["timezone"])
    gsNetworkErrors = spreadsheet.worksheet("title", sheetsConfig["errors"])

def epochToTime(usertimezone, theEpoch):
    """This Function converts the Epoch based timestamp, and converts it to a datetime string"""
    # get time in UTC
    utc_dt = datetime.datetime.utcfromtimestamp(
        theEpoch).replace(tzinfo=pytz.utc)

    # convert it to tz
    tz = pytz.timezone(usertimezone)
    dt = utc_dt.astimezone(tz)

    # print it
    shiftedTime = dt.strftime('%Y-%m-%d %H:%M:%S')
    return shiftedTime


def sales_sheets_handling(user, price, theEpoch):
    """This function handles selling price data being added to the spreadsheet and pushing the spreadsheet"""
    usertimezoneCheck = userTzCheck(user)
    usertimezone = None
    if usertimezoneCheck == False:
        usertimezone = "UTC"
    else:
        usertimezone = usertimezoneCheck
    correctedTime = epochToTime(usertimezone, theEpoch)
    the_stuff = [user, price, correctedTime, theEpoch, usertimezone]
    gsSalesWorksheet.link(syncToCloud=True)
    # this gets all the cells in the Worksheet
    worksheetAllValues = gsSalesWorksheet.get_all_values()
    # this checks for all the elements in the list, since each row is a set of elements within the main list
    rowNumbs = len(worksheetAllValues)
    # this creates the next cell number available for usage.
    latestRowNumb = rowNumbs + 1
    # this puts the information provided by the user, in the right cell
    gsSalesWorksheet.update_row(latestRowNumb, the_stuff)
    # This adds 1 more row, to make sure we dont run out of rows for information.
    gsSalesWorksheet.add_rows(1)


def purchase_sheets_handling(user, price, theEpoch):
    """This function handles buying price data being added to the spreadsheet and pushing the spreadsheet"""
    usertimezoneCheck = userTzCheck(user)
    usertimezone = None
    if usertimezoneCheck == False:
        usertimezone = "UTC"
    else:
        usertimezone = usertimezoneCheck
    correctedTime = epochToTime(usertimezone, theEpoch)
    the_stuff = [user, price, correctedTime, theEpoch, usertimezone]
    gsPurchaseWorksheet.link(syncToCloud=True)
    # this gets all the cells in the Worksheet
    worksheetAllValues = salesSheetValues()
    # this checks for all the elements in the list, since each row is a set of elements within the main list
    rowNumbs = len(worksheetAllValues)
    # this creates the next cell number available for usage.
    latestRowNumb = rowNumbs + 1
    # this puts the information provided by the user, in the right cell
    gsPurchaseWorksheet.update_row(latestRowNumb, the_stuff)
    # This adds 1 more row, to make sure we dont run out of rows for information.
    gsPurchaseWorksheet.add_rows(1)

def salesSheetValues():
    """This function simply gets all the values of the sales spreadsheet spreadsheet"""
    worksheetAllValues = gsSalesWorksheet.get_all_values()
    return worksheetAllValues


def priceCheck(theEpoch):
    salesWorksheet = salesSheetValues()
    for i in salesWorksheet:
        print(i)


def has_admin_privilege():
    """Check that returns true if user has admin permissions"""
    async def predicate(ctx):
        return await (bot.is_owner(ctx.author) or
                      ctx.author.permissions_in(ctx.channel).administrator)
    return commands.check(predicate)


def userTzCheck(user):
    """This function will check if the user has a timezone set or not. If they have a TZ, it will return the Pytz timezone, if not, it'll return false"""
    timeWorksheetValues = gsUserTimezones.get_all_values()
    user_tz = None
    for i in timeWorksheetValues:
        if user == i[0]:
            user_tz = i[1]
    if user_tz == None:
        user_tz = False
    return user_tz


def userTzUpdater(user, usertimezone):
    checkResponse = userTzCheck(user)
    the_stuff = [user, usertimezone]
    # this gets all the cells in the Worksheet
    worksheetAllValues = gsUserTimezones.get_all_values()
    # this checks for all the elements in the list, since each row is a set of elements within the main list
    rowNumbs = len(worksheetAllValues)
    if checkResponse == False:
        # this creates the next cell number available for usage.
        latestRowNumb = rowNumbs + 1
        # this puts the information provided by the user, in the right cell
        gsUserTimezones.update_row(latestRowNumb, the_stuff)
        # This adds 1 more row, to make sure we dont run out of rows for information.
        gsUserTimezones.add_rows(1)
        tzmessage1 = "Your time zone has been added"
        return tzmessage1
    elif checkResponse is not usertimezone:  # this will eventually find and replace a User's timezone, however i was having issues with it. if it needs to be changed i will have to do it manually, not fun, but on a small scale it should be fine. This will need a fair bit of documentation reading.
        tzmessage2 = "the usertimezone update feature is being worked on. If you would like your user timezone updated currently, please contact ethanbreck#3465, or if you know python, please help develop this feature."
        return tzmessage2
    # this one just verifies that the timezone that the user wants to set is already set, and they dont need to change a thing.
    elif checkResponse == usertimezone:
        tzmessage3 = "Your user timezone is up to date"
        return tzmessage3


def errorReporting(errorReport):
    updatedReport = errorReport
    worksheetAllValues = gsNetworkErrors.get_all_values()
    print(worksheetAllValues)
    rowNumbs = len(worksheetAllValues)
    latestRowNumb = rowNumbs + 1
    gsNetworkErrors.update_row(latestRowNumb, updatedReport)
    gsNetworkErrors.add_rows(1)



@bot.event
async def on_ready():
    os.system("echo Logged in as {0.user}".format(bot))


@bot.command()
@has_admin_privilege()
async def tzlist(ctx):
    """This function lists current accepted timezones"""
    with open("timezones/timezone0.txt", mode="r") as tzlist1:
        tzlist1content = tzlist1.read()
    with open("timezones/timezone1.txt", mode="r") as tzlist2:
        tzlist2content = tzlist2.read()
    with open("timezones/timezone2.txt", mode="r") as tzlist3:
        tzlist3content = tzlist3.read()
    with open("timezones/timezone3.txt", mode="r") as tzlist4:
        tzlist4content = tzlist4.read()
    with open("timezones/timezone4.txt", mode="r") as tzlist5:
        tzlist5content = tzlist5.read()
    with open("timezones/timezone5.txt", mode="r") as tzlist6:
        tzlist6content = tzlist6.read()
    with open("timezones/timezone6.txt", mode="r") as tzlist7:
        tzlist7content = tzlist7.read()
    await ctx.send(tzlist1content)
    await ctx.send(tzlist2content)
    await ctx.send(tzlist3content)
    await ctx.send(tzlist4content)
    await ctx.send(tzlist5content)
    await ctx.send(tzlist6content)
    await ctx.send(tzlist7content)


@bot.command()
async def tzcheck(ctx):
    """This function checks and lists your timezone"""
    await ctx.send("Checking person")
    username = ctx.author.name
    userdiscrim = ctx.author.discriminator
    user = username + "#" + userdiscrim
    tz_stuff = userTzCheck(user)
    user_usertimezone = None
    if tz_stuff == False:
        user_usertimezone = "No user timezone Set"
    else:
        user_usertimezone = tz_stuff
    await ctx.send("Your Current user timezone: " + user_usertimezone)


@bot.command()
async def buffering(ctx):
    """This tracks when the stream is buffering"""
    username = ctx.author.name
    userdiscrim = ctx.author.discriminator
    user = username + "#" + userdiscrim
    theEpoch = time.time()
    currentTime = epochToTime("America/Los_Angeles", theEpoch)
    theReport = [user, currentTime, "Buffering"]
    await ctx.send(theReport)
    errorReporting(theReport)

@bot.command()
async def los(ctx):
    """This command tracks network errors and such"""
    username = ctx.author.name
    userdiscrim = ctx.author.discriminator
    user = username + "#" + userdiscrim
    theEpoch = time.time()
    currentTime = epochToTime("America/Los_Angeles", theEpoch)
    theReport = [user, currentTime, "Signal Lost"]
    print(theReport)
    await ctx.send(theReport)
    errorReporting(theReport)

@bot.command()
async def ethan(ctx):
    username = ctx.author.name
    userdiscrim = ctx.author.discriminator
    user = username + "#" + userdiscrim
    await ctx.send("That works I guess @{}".format(user))

@bot.command()
async def tzupdate(ctx, usertimezone: str):
    """This command checks and updates the user timezone."""
    username = ctx.author.name
    userdiscrim = ctx.author.discriminator
    user = username + "#" + userdiscrim
    tzupdate = userTzUpdater(user, usertimezone)
    await ctx.send(tzupdate)


@bot.command()
async def openthepodbaydoors(ctx):
    username = ctx.author.name
    userdiscrim = ctx.author.discriminator
    user = username + "#" + userdiscrim
    await ctx.send("Im sorry {}, Im afraid I can't do that".format(user))

@bot.command()
async def whydoesthisexist(ctx):
    username = ctx.author.name
    userdiscrim = ctx.author.discriminator
    user = username + "#" + userdiscrim
    await ctx.send("I dont know {}, why do any of us exist?".format(user))

@bot.command()
async def salesSpreadsheet(ctx):
    """This outputs the current sales spreadsheet"""
    salesValues = salesSheetValues()
    sheetURL = "https://docs.google.com/spreadsheets/d/1OQvZv-LtUy7C2K6yip6u5tij4J0dP8sXdV23Cj6F2vY/edit?usp=sharing"
    await ctx.send(sheetURL)

@bot.command()
async def sell(ctx, price: int):
    """'!sell {$} the $ being a number"""
    theEpoch = time.time()
    username = ctx.author.name
    userdiscrim = ctx.author.discriminator
    user = username + "#" + userdiscrim
    await ctx.send("Logging {}".format(price))
    os.system(
        "echo Sales price Logged. User: {}, Price: {}, epochtime: {}".format(
            user,
            price,
            theEpoch))
    sales_sheets_handling(user, price, theEpoch)


@bot.command()
async def buy(ctx, price: int):
    """'!buy {$} with the $ being a number"""
    theEpoch = time.time()
    username = ctx.author.name
    userdiscrim = ctx.author.discriminator
    user = username + "#" + userdiscrim
    await ctx.send("Logging {}".format(price))
    os.system(
        "echo Purchase price Logged. User: {}, Price: {}, epochtime: {}".format(
            user,
            price,
            theEpoch))
    purchase_sheets_handling(user, price, theEpoch)


@bot.command()
@has_admin_privilege()
async def reboot(ctx):
    """Admins use this to reboot the bot"""
    await ctx.send("Rebooting!...")
    await bot.logout()
    sys.exit(0)


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