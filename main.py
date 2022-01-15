# ---------------------------------------------------------- Imports
import discord
from discord.ext import commands

import os
import random
import json

from revive import keep_alive

# ---------------------------------------------------------- Variables

defaultPrefix = '!'

dev = "Shuppin#0001"

# ---------------------------------------------------------- Initialisation

def getPrefix(bot, message):

  with open("prefrences.json", "r") as f:
    prefs = json.load(f)

  if isinstance(message.channel, discord.channel.DMChannel):
    return defaultPrefix
  else:
    if str(message.guild.id) in prefs.keys():
      return prefs[str(message.guild.id)]['prefix']
    else:
      return defaultPrefix

activity = discord.Activity(type=discord.ActivityType.listening, name="your commands.")
bot = commands.Bot(command_prefix=getPrefix,activity=activity, status=discord.Status.online)

# ---------------------------------------------------------- Event Handling

@bot.event
async def on_ready():
  print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
  if message.author == bot.user:
    return

  if "<@!851132992289898508>" in message.content or "<@851132992289898508>" in message.content:
    responses = ["Hey, do you Want know how to keep an idiot waiting….I’ll tell you tomorrow.", "I fail to see why I should give two hoots about your opinion", "You can do better than that? Surely.", "Do you not have a smarter choice of words than that?", "Well that's not very nice :(", "After all I have done for you? You treat me as such a low being?"]

    if any(word in message.content for word in ["bad", "trash", "stupid", "idiot"]):
        await message.channel.send(random.choice(responses))

  await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.errors.NoPrivateMessage):
    await ctx.send("You can't perform that command here!")

@bot.event
async def on_guild_join(guild):

  with open("prefrences.json", "r") as f:
    prefs = json.load(f)

  prefs[str(guild.id)] = {}
  prefs[str(guild.id)]['prefix'] = defaultPrefix
  prefs[str(guild.id)]['confessionChannel'] = None

  with open("prefrences.json", "w") as f:
    json.dump(prefs, f, indent=4)

@bot.event
async def on_guild_remove(guild):

  with open("prefrences.json", "r") as f:
    prefs = json.load(f)

  try:
    del prefs[str(guild.id)]
  except KeyError:
    print(f"Error: File '{os.path.basename(__file__)}' in on_guild_remove() | '{guild.name}' ({guild.id}) attempted to remove guild information where none exists")

  with open("prefrences.json", "w") as f:
    json.dump(prefs, f, indent=4)

# ---------------------------------------------------------- Execution

if __name__ == '__main__':
  for filename in os.listdir('./cogs'):
    if filename.endswith(".py"):
      bot.load_extension(f"cogs.{filename[:-3]}")

  #keep_alive()
  bot.run(os.environ['TOKEN'])


# ---------------------------------------------------------- To do
#
# Confession Bot
#
# Functionality
#
#    JSON Guild prefrences ✅
#    Permission Handling ✅
#    DM responses
#      Basic DM Handling 😐
# 
# Utility Commands ✅
# 
#   ping ✅
#   changeprefix ✅
# 
# Game commands
# 
#  Setup
#   setChannel ✅
#   removeChannel ✅
#   getChannel ✅
#  
#  Channel specific
#   confession			- DMs?
#   removeConfession (user)
#   removeConfession (admin)
# 
#  Interaction
#    guess
#
