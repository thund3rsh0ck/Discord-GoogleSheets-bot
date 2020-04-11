'''This is a bot that integrations google sheets with discord API. This Version uses the very base of the Repo it's forked from, but diverges a lot to track and report turnip prices for Animal Crossing New Horizons (ACNH)'''
# Python Libraries
import time
import os
import sys
import datetime

# Pipfile Libraries
import gspread
import requests
import discord
import yaml

from typing import Mapping, Any

from discord.ext import commands
from oauth2client.service_account import ServiceAccountCredentials

app_dir = os.path.abspath(os.path.dirname(__file__))
token_file = os.path.join(app_dir, "discordconfig.yaml")

with open(token_file, mode="r") as discordfile:
    discordCreds: Mapping[str, Any] = yaml.load(discordfile, Loader=yaml.FullLoader)
    token, prefix = discordCreds["token"], discordCreds["prefix"]

bot = commands.Bot(command_prefix=prefix, pm_help=None,
                        case_insensitive=False)

def has_admin_privilege():
    """Check that returns true if user has admin permissions"""
    async def predicate(ctx):
        return await (bot.is_owner(ctx.author) or \
               ctx.author.permissions_in(ctx.channel).administrator)
    return commands.check(predicate)

@bot.command()
@has_admin_privilege()
async def reboot(ctx):
	await ctx.send("Rebooting!...")
	await bot.logout()
	sys.exit(0)


@bot.event
async def on_ready():
	print('Logged in as {0.user}'.format(bot))


@bot.command()
async def price(ctx, price: int):
	"""This is the help for price. \n Please format things '!price {#}' without any other characters"""
	await ctx.send("Logging {}".format(price))



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
	bot.run(token, bot=True, reconnect=True)
