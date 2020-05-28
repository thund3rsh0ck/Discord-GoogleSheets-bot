'''This file was a test done by a developer working on this project, and is not meant to be used at all for bot usage. Use bot.py for the bot.'''
# Python Libraries
import time
import os
import sys
import datetime
import logging
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
discord_file = os.path.join(app_dir, "config.yaml")

with open(discord_file, mode="r") as discordfile:
    discordCreds: Mapping[str, Any] = yaml.load(
        discordfile, Loader=yaml.FullLoader)
    token, prefix = discordCreds["token"], discordCreds["prefix"]



gsClient = None  # google sheets client
# google sheets worksheet that corresponds to the selling price table
gsSalesWorksheet = None
# google sheet worksheet that corresponds to the purchasing price table
gsPurchaseWorksheet = None
# google sheet that corresponds to discord users Pytz timezone data
gsUserTimezones = None
# google sheets that corresponds to error reporting.
gsNetworkErrors = None

# Logging setup

LOGLEVEL = os.environ.get("LOGLEVEL", "INFO").upper()
logger = logging.getLogger(__name__)
logger.setLevel(LOGLEVEL)
fmt = logging.Formatter("%(asctime)s %(funcName)s %(levelname)s %(message)s")
ch = logging.StreamHandler()
fh = logging.FileHandler('thebot.log')
ch.setFormatter(fmt)
fh.setFormatter(fmt)
logger.addHandler(fh)
logger.addHandler(ch)


# create bot
bot = commands.Bot(command_prefix=prefix, pm_help=None,
                   case_insensitive=False)

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
    channel = await bot.fetch_channel(715296923136950344)
    await channel.send("q")


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
async def yucca(ctx):
    username = ctx.author.name
    await ctx.send("Thats pretty Yucca {}".format(username))



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
async def tzupdate(ctx, usertimezone: str):
    """This command checks and updates the user timezone."""
    username = ctx.author.name
    userdiscrim = ctx.author.discriminator
    user = username + "#" + userdiscrim
    tzupdate = userTzUpdater(user, usertimezone)
    await ctx.send(tzupdate)

@bot.command(pass_context=True)
async def ethan(ctx):
    """The meme command that does nothing"""
    await ctx.send("That works I guess {}".format(ctx.message.author.mention))

@bot.command(pass_context=True)
async def quoteadd(ctx, quote: str=""):
	if quote != "":
		a_file = open("quotes.json", "r")
		quotes = json.load(a_file)
		a_file.close()
		quoteid = len(quotes["quotes"])
		quotejson = {
		"id": quoteid,
		"quote": quote
		}
		quotes["quotes"].append(quotejson)
		a_file = open("quotes.json", "w")
		json.dump(quotes, a_file)
		a_file.close()
		await ctx.send("Quote added at position **" + str(quoteid) +"**  {}".format(ctx.message.author.mention))
	else:
		await ctx.send("You didn't quote anything {}".format(ctx.message.author.mention))

@bot.command(pass_context=True)
async def quote(ctx, quoteid: str=""):
	if quoteid != "":
		a_file = open("quotes.json", "r")
		quotes = json.load(a_file)
		a_file.close()
		if int(quoteid) < len(quotes["quotes"]):
			quote = quotes["quotes"][int(quoteid)]
			if quote != None:
				await ctx.send("Quote number "+quoteid +": **" + str(quote["quote"])+ "**")
			else:
				await ctx.send("Quote number **"+quoteid +"** was removed")
		else:
			await ctx.send("There is no quote in position **"+ quoteid +"** {}".format(ctx.message.author.mention))
	else:
		await ctx.send("You didn't quote anything {}".format(ctx.message.author.mention))


@bot.command(pass_context=True)
async def quoterem(ctx, quoteid: str=""):
	if quoteid != "":
		a_file = open("quotes.json", "r")
		quotes = json.load(a_file)
		a_file.close()
		if int(quoteid) < len(quotes["quotes"]):
			quotes["quotes"][int(quoteid)]["quote"] = None
			a_file = open("quotes.json", "w")
			json.dump(quotes, a_file)
			a_file.close()
			await ctx.send("Quote number **"+quoteid +"** was removed")
		else:
			await ctx.send("There is no quote in position **"+ quoteid +"** {}".format(ctx.message.author.mention))
	else:
		await ctx.send("You didn't quote anything {}".format(ctx.message.author.mention))

@bot.command(pass_context=True)
async def quotes(ctx):
	a_file = open("quotes.json", "r")
	quotes = json.load(a_file)
	a_file.close()
	message = ""
	embed = discord.Embed(title="Quotes", description=" {}".format(ctx.message.author.mention), color=0x00ff00)
	for quote in quotes["quotes"]:
		embed.add_field(name="Quote number: " + str(quote["id"]), value=quote["quote"], inline=False)
	await ctx.send(embed=embed)

@bot.command()
async def openThePodBayDoors(ctx):
    """This opens the Pod Bay Doors"""
    username = ctx.author.name
    user = username
    await ctx.send("Im sorry {}, Im afraid I can't do that".format(user))

@bot.command()
async def whyDoesThisExist(ctx):
    """Asking the Real Questions"""
    username = ctx.author.name
    user = username
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
    user = username
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
    user = username
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

    username = ctx.author.name
    user = username

    if isinstance(error, commands.CommandNotFound):
        # get message text
        return await ctx.send("Unknown command. Type {}help for help.".format(prefix))
    elif isinstance(error, commands.CheckFailure):
        return await ctx.send("I'm sorry {} I can't do that".format(user))
    else:
        raise error


if __name__ == "__main__":
    bot.run(token, bot=True, reconnect=True)