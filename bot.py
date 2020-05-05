#!/usr/bin/python
#Comment added to tell bash what interpreter to use when in a *nix environment -Cletus
import discord
from discord.ext import commands
import asyncio
import sys
import os
import argparse

#Placeholder variable(s)
name = "Oak Bot"

#Parse Args
parser = argparse.ArgumentParser(description='Connects to discord and acts as the interactive layer between the discord users and the bot.',prog='bot.py')
parser.add_argument("token", type=str, help="Bot Token as String.")
parser.add_argument("id", type=int, help="Admin ID as Integer.")
parser.add_argument("-n", "--name", help="Provide an alternative name to use in public chat.")
parser.add_argument("-v", "--verbose", help="Additional Verbosity.",action='store_true')
args = parser.parse_args()

#Assign arguments to appropriate variables
TOKEN = args.token
ID = args.id

if args.verbose:
    print("Token passed: ", TOKEN)
    print("ID Passed: ", ID)

if args.name:
    name = args.name
    print("Provided alternative name: ",name)

client = commands.Bot(command_prefix = '$')
client.remove_command('help')

extensions = ['RaidCommands']

@client.event
async def on_ready():
    print('Logged in as', client.user.name, "with an id of", client.user.id, "and a nickname of", name)
    print('------')

@client.event
async def on_message(message):
	if message.author == client.user:
		return
	channel = message.channel
	if message.guild is None:
		await message.channel.send("Hey there!")
	else:
	    await client.process_commands(message)

#Command used for bot admin to turn their bot off
#Please put the admin's discord ID where indicated
@client.command()
async def logout(ctx):
	if ctx.message.author.id in [ID]:
		await ctx.send('```Shutting down...```')
		await client.logout()
	else:
		await ctx.send('Nice try jackass!')
		
#Sends greet command
@client.command()
async def greet(ctx):
	await ctx.send("Hello everyone! I am", name, "and I'm here to assist you :)")

@client.command()
async def load(extension):
	try:
		client.load_extension(extension)
		print('Loaded {}'.format(extension))
	except Exception as error:
		print('{} cannot be loaded. [{}]'.format(extension, error))

@client.command()
async def unload(extension):
	try:
		client.unload_extension(extension)
		print('Unloaded {}'.format(extension))
	except Exception as error:
		print('{} cannot be unloaded. [{}]'.format(extension, error))

async def test():
	while True:
		print("Hello!")
		await asyncio.sleep(1)

if __name__ == '__main__':
	for extension in extensions:
		try:
			client.load_extension(extension)
		except Exception as error:
			print('{} cannot be loaded. [{}]'.format(extension, error))

	#client.loop.create_task(test())
	client.run(TOKEN)
