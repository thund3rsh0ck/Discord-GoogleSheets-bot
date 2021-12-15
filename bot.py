'''This is a bot that integrations google sheets with discord API. It was intended to track participation for a game called CATS for Android but could be used for anything'''
import discord
import time
import config
from config import token, link, prefix, ownerid
from discord.ext.commands import Bot
import requests
import gspread
import datetime
from oauth2client.service_account import ServiceAccountCredentials

# Global Variables
global war_start_date
war_start_date=str(datetime.datetime.today().strftime('%m/%d/%Y'))

client = Bot(prefix)

for i in range(500):
	while True:
		try:

			@client.event
			async def on_ready():
				print("----------------------")
				print("Logged In As")
				print("Username: %s"%client.user.name)
				print("ID: %s"%client.user.id)
				print("----------------------")


				
			@client.command()
			async def ping(ctx):
				'''See if The Bot is Working'''
				await ctx.send(f'Pong! In {round(client.latency * 1000)}ms')
				
			@client.command()
			async def participation():
				'''Shows participation stats for all players in current war'''
				global war_start_date
				scope = ['https://spreadsheets.google.com/feeds',
					 'https://www.googleapis.com/auth/drive']
			    '''insert link to json file with google creds below'''
				credentials = ServiceAccountCredentials.from_json_keyfile_name('c:\tmp\samplejsonfile.json', scope)
				gc = gspread.authorize(credentials)
				wks = gc.open("City Kings Participation")
				worksheet = wks.worksheet("summary")
				memberlist ="This is a list of everyone and their participation in the war started on "+war_start_date+"\n"
				cell_list = worksheet.col_values(1)
				participation_date = worksheet.col_values(5)
				participation_percent = worksheet.col_values(3)
				war_count = worksheet.col_values(4)
				makememberlistcounter = 1
				while makememberlistcounter < len(cell_list):
					if(participation_date[makememberlistcounter]==war_start_date):
						memberlist += (str(makememberlistcounter)+'. '+cell_list[makememberlistcounter]+" :white_check_mark: - Overall Participation: "+participation_percent[makememberlistcounter]+" ("+ war_count[makememberlistcounter]+" wars)"+"\n")
					else:
						memberlist += (str(makememberlistcounter)+'. '+cell_list[makememberlistcounter]+" :x: - Overall Participation: "+participation_percent[makememberlistcounter]+" ("+ war_count[makememberlistcounter]+" wars)"+"\n")
					makememberlistcounter+=1
				await client.say(memberlist)
				await client.say("If you want to update participation in current war, use ~update [number],[number],[number]")
				
			@client.command()
			async def active():
				'''Shows members who have participated in current war'''
				global war_start_date
				scope = ['https://spreadsheets.google.com/feeds',
					 'https://www.googleapis.com/auth/drive']
				credentials = ServiceAccountCredentials.from_json_keyfile_name('c:\tmp\samplejsonfile.json', scope)
				gc = gspread.authorize(credentials)
				wks = gc.open("City Kings Participation")
				worksheet = wks.worksheet("summary")
				memberlist ="This is a list of everyone and their participation in the war started on "+war_start_date+"\n"
				participatedlist="This is a list of everyone who was active in the war started "+war_start_date+"\n"
				notparticipatedlist="This is a list of everyone who was not active in the war started "+war_start_date+"\n"
				cell_list = worksheet.col_values(1)
				participation_date = worksheet.col_values(5)
				makememberlistcounter = 1
				while makememberlistcounter < len(cell_list):
					if(participation_date[makememberlistcounter]==war_start_date):
						participatedlist += (str(makememberlistcounter)+'. '+cell_list[makememberlistcounter]+" :white_check_mark: "+"\n")
					makememberlistcounter+=1
				await client.say(participatedlist)
				
			@client.command()
			async def inactive():
				'''Shows members who have not participated in current war'''
				global war_start_date
				scope = ['https://spreadsheets.google.com/feeds',
					 'https://www.googleapis.com/auth/drive']
				credentials = ServiceAccountCredentials.from_json_keyfile_name('c:\tmp\samplejsonfile.json', scope)
				gc = gspread.authorize(credentials)
				wks = gc.open("City Kings Participation")
				worksheet = wks.worksheet("summary")
				memberlist ="This is a list of everyone and their participation in the war started on "+war_start_date+"\n"
				participatedlist="This is a list of everyone who was active in the war started "+war_start_date+"\n"
				notparticipatedlist="This is a list of everyone who was not active in the war started "+war_start_date+"\n"
				cell_list = worksheet.col_values(1)
				participation_date = worksheet.col_values(5)
				makememberlistcounter = 1
				while makememberlistcounter < len(cell_list):
					if(participation_date[makememberlistcounter]==war_start_date):
						participatedlist += (str(makememberlistcounter)+'. '+cell_list[makememberlistcounter]+" :white_check_mark: "+"\n")
					else:
						notparticipatedlist += (str(makememberlistcounter)+'. '+cell_list[makememberlistcounter]+" :x: "+"\n")
					makememberlistcounter+=1
				await client.say(notparticipatedlist)
				await client.say("If you want to update this list, use ~update [number],[number],[number]")
				
			@client.command()
			async def newwar():
				'''Use this if we start a new round of city wars'''
				global war_start_date
				war_start_date=str(datetime.datetime.today().strftime('%m/%d/%Y'))
				await client.say('Setting war start date to today, '+str(war_start_date))
				
			@client.command()
			async def oldwar():
				'''only use this if you accidentally used newwar too early'''
				now = datetime.datetime.now()
				global war_start_date
				month=str(now.month)
				if len(month)==1:
					month="0"+month
				day=str(int(now.day)-1)
				if len(day)==1:
					day="0"+day
				war_start_date=(str(month)+"/"+str(day)+"/"+str(now.year))
				await client.say('Setting war start date to yesterday, '+str(war_start_date))
				
			@client.command(pass_context=True)
			async def update(context,number):
				'''Updates participation in current war, usage: ~update 1,2,10,15'''
				global war_start_date
				scope = ['https://spreadsheets.google.com/feeds',
					 'https://www.googleapis.com/auth/drive']
				credentials = ServiceAccountCredentials.from_json_keyfile_name('c:\tmp\samplejsonfile.json', scope)
				gc = gspread.authorize(credentials)
				wks = gc.open("City Kings Participation")
				worksheet = wks.worksheet("summary")
				memberlist ="This is a list of everyone and their participation in the war started on "+war_start_date+"\n"
				participatedlist="This is a list of everyone who was active in the war started "+war_start_date+"\n"
				notparticipatedlist="This is a list of everyone who was not active in the war started "+war_start_date+"\n"
				cell_list = worksheet.col_values(1)
				participation_date = worksheet.col_values(5)
				makememberlistcounter = 1
				while makememberlistcounter < len(cell_list):
					if(participation_date[makememberlistcounter]==war_start_date):
						participatedlist += (str(makememberlistcounter)+'. '+cell_list[makememberlistcounter]+" :white_check_mark: "+"\n")
					else:
						notparticipatedlist += (str(makememberlistcounter)+'. '+cell_list[makememberlistcounter]+" :x: "+"\n")
					makememberlistcounter+=1
				#validate input
				if (")" not in number) and ("+" not in number):
					#if there are multiple numbers
					if ("," in number):
						counter = 1
						#catch first number
						firstcommalocation=number.find(",")
						#print (firstcommalocation)
						firstindex=int(number[:int(firstcommalocation)])
						#print (firstindex)
						playername=cell_list[firstindex]
						if (str(participation_date[firstindex]) != str(war_start_date)):
							worksheet = wks.worksheet("data")
							datacell_list = worksheet.col_values(1)
							worksheet.update_cell(len(datacell_list)+1, 1, playername)
							worksheet.update_cell(len(datacell_list)+1, 2, war_start_date)
							worksheet.update_cell(len(datacell_list)+1, 6, str(context.message.author))
							await client.say(' :white_check_mark: '+playername+' has been marked as active in the war starting on: '+war_start_date)
						else:
							playername=cell_list[firstindex]
							await client.say(':x: ERROR: '+playername+' has been already participated in the war starting on: '+war_start_date)
						#run through all but last number
						while counter<26:
							if (","+str(counter)+",") in number:
								playername=cell_list[int(counter)]
								if (str(participation_date[int(counter)]) != str(war_start_date)):
									worksheet = wks.worksheet("data")
									datacell_list = worksheet.col_values(1)
									worksheet.update_cell(len(datacell_list)+1, 1, playername)
									worksheet.update_cell(len(datacell_list)+1, 2, war_start_date)
									worksheet.update_cell(len(datacell_list)+1, 6, str(context.message.author))
									await client.say(' :white_check_mark: '+playername+' has been marked as active in the war starting on: '+war_start_date)
								else:
									playername=cell_list[int(counter)]
									await client.say(':x: ERROR: '+playername+' has been already participated in the war starting on: '+war_start_date)
							counter += 1

						#catch last number
						if number[len(number)-2:len(number)-1]==",":
							playername=cell_list[int(number[len(number)-1:])]
							if (str(participation_date[int(number[len(number)-1:])]) != str(war_start_date)):
								worksheet = wks.worksheet("data")
								datacell_list = worksheet.col_values(1)
								worksheet.update_cell(len(datacell_list)+1, 1, playername)
								worksheet.update_cell(len(datacell_list)+1, 2, war_start_date)
								worksheet.update_cell(len(datacell_list)+1, 6, str(context.message.author))
								await client.say(' :white_check_mark: '+playername+' has been marked as active in the war starting on: '+war_start_date)
							else:
								playername=cell_list[int(number[len(number)-1:])]
								await client.say(':x: ERROR: '+playername+' has been already participated in the war starting on: '+war_start_date)
						elif number[len(number)-3:len(number)-2]==",":
							playernumber = int(number[len(number)-2:])
							#print (playernumber)
							playername=cell_list[playernumber]
							#print (playername)
							if (str(participation_date[playernumber]) != str(war_start_date)):
								worksheet = wks.worksheet("data")
								datacell_list = worksheet.col_values(1)
								worksheet.update_cell(len(datacell_list)+1, 1, playername)
								worksheet.update_cell(len(datacell_list)+1, 2, war_start_date)
								worksheet.update_cell(len(datacell_list)+1, 6, str(context.message.author))
								await client.say(' :white_check_mark: '+playername+' has been marked as active in the war starting on: '+war_start_date)
							else:
								playername=cell_list[int(number[len(number)-2:])]
								await client.say(':x: ERROR: '+playername+' has been already participated in the war starting on: '+war_start_date)
						else:
							await client.say(":x: ERROR: You entered an invalid input")
					else:
						if (str(participation_date[int(number)]) != str(war_start_date)):
							playername=cell_list[int(number)]
							worksheet = wks.worksheet("data")
							cell_list = worksheet.col_values(1)
							worksheet.update_cell(len(cell_list)+1, 1, playername)
							worksheet.update_cell(len(cell_list)+1, 2, war_start_date)
							worksheet.update_cell(len(cell_list)+1, 6, str(context.message.author))
							await client.say(' :white_check_mark: '+playername+' has been marked as active in the war starting on: '+war_start_date)
						else:
							playername=cell_list[int(number)]
							await client.say(':x: ERROR: '+playername+' has been already participated in the war starting on: '+war_start_date)
				else:
					await client.say(":x: ERROR: You entered an invalid input")
			client.run(token)
			break
		except Exception: # Replace Exception with something more specific.
			continue
			
