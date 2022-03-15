from nextcord.ext import commands

import json
import os
import random

defaultPrefix = '-'

class _events(commands.Cog):
  
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    print(f"Logged in as {self.bot.user}")

  @commands.Cog.listener()
  async def on_message(self, message):
    if message.author == self.bot.user:
      return

    if "<@!851132992289898508>" in message.content or "<@851132992289898508>" in message.content:
      responses = ["Hey, do you Want know how to keep an idiot waiting….I’ll tell you tomorrow.", "I fail to see why I should give two ||redacted|| about your opinion", "You can do better than that? Surely.", "Do you not have a smarter choice of words than that?", "Well that's not very nice :(", "After all I have done for you? You treat me as such a low being?"]

      if any(word in message.content for word in ["bad", "trash", "stupid", "idiot", "dumb"]):
          await message.channel.send(random.choice(responses))

  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
    if isinstance(error, commands.errors.NoPrivateMessage):
      await ctx.send("You can't perform that command here!")

  @commands.Cog.listener()
  async def on_guild_join(self, guild):

    with open("prefrences.json", "r") as f:
      prefs = json.load(f)

    prefs[str(guild.id)] = {}
    prefs[str(guild.id)]['prefix'] = defaultPrefix
    prefs[str(guild.id)]['confessionChannel'] = None
    prefs[str(guild.id)]['confessions'] = []

    with open("prefrences.json", "w") as f:
      json.dump(prefs, f, indent=4)

  @commands.Cog.listener()
  async def on_guild_remove(self, guild):

    with open("prefrences.json", "r") as f:
      prefs = json.load(f)

    try:
      del prefs[str(guild.id)]
    except KeyError:
      print(f"Error: File '{os.path.basename(__file__)}' in _events.on_guild_remove() | '{guild.name}' ({guild.id}) attempted to remove guild information where none exists")

    with open("prefrences.json", "w") as f:
      json.dump(prefs, f, indent=4)


def setup(client):
  client.add_cog(_events(client))
  print(f"Module '{os.path.basename(__file__)}' initialised")