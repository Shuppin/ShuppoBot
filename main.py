import nextcord as discord
from nextcord.ext import commands

import os
import json

import server

defaultPrefix = '-'

dev = "Shuppin#0001"

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

if __name__ == '__main__':

  intents = discord.Intents.default()
  intents.members = True
  activity = discord.Activity(type=discord.ActivityType.playing, name="uptime testing")
  bot = commands.Bot(command_prefix=getPrefix,activity=activity, status=discord.Status.online, intents=intents)

  for filename in os.listdir('./cogs'):
    if filename.endswith(".py"):
      bot.load_extension(f"cogs.{filename[:-3]}")

  #server.keep_alive()
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
