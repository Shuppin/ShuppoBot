import nextcord as discord
from nextcord.ext import commands
from nextcord.ext.commands import has_permissions

import json
import os

dev = "Shuppin#0001"


class ConfessionConfig(commands.Cog):
  
  def __init__(self, bot):
    self.bot = bot

  @commands.guild_only()
  @commands.command(aliases=["setChannel","setchannel","setconfessionChannel","setConfessionchannel", "setconfessionchannel"])
  @has_permissions(administrator=True)
  async def setConfessionChannel(self, ctx, channelArg: str):

    with open(os.getcwd() + "/prefrences.json", "r") as f:
      prefs = json.load(f)

    if type(discord.utils.get(ctx.guild.channels, name=channelArg)) == discord.channel.TextChannel:

      channel = discord.utils.get(ctx.guild.channels, name=channelArg)

      prefs[str(ctx.guild.id)]["confessionChannel"] = str(channel.id)

      await ctx.send(f"Set confession channel to <#{str(channel.id)}>")

    else:

      if channelArg.startswith("<#"):
        channelArg = channelArg[2:-1]

      try:

        channelArg = int(channelArg)

        if type(self.bot.get_channel(channelArg)) == discord.channel.TextChannel:

          channel = self.bot.get_channel(channelArg)
          prefs[str(ctx.guild.id)]["confessionChannel"] = str(channel.id)
          await ctx.send(f"Set confession channel to <#{str(channel.id)}>")

      except Exception:
        await ctx.send(f"Could not find channel '{channelArg}' ")

    with open(os.getcwd() + "/prefrences.json", "w") as f:
      json.dump(prefs, f, indent=4)

  @commands.guild_only()
  @commands.command(aliases=["getChannel", "getchannel", "getconfessionchannel", "getconfessionChannel", "getConfessionchannel"])
  async def getConfessionChannel(self, ctx):
    
    with open(os.getcwd() + "/prefrences.json", "r") as f:
      prefs = json.load(f)
    
    if prefs[str(ctx.guild.id)]["confessionChannel"] != None:

      if type(self.bot.get_channel(prefs[str(ctx.guild.id)]["confessionChannel"])) == None:
        prefs[str(ctx.guild.id)]["confessionChannel"] = None
        await ctx.send(f"No confession channel is currently set, Use `{prefs[str(ctx.guild.id)]['prefix']}setConfessionChannel` to assign one.")

      with open(os.getcwd() + "/prefrences.json", "w") as f:
        json.dump(prefs, f, indent=4)

      confessionChannelID = prefs[str(ctx.guild.id)]["confessionChannel"]

      try:
        confessionChannel = self.bot.get_channel(int(confessionChannelID))

        if confessionChannel != None:
          await ctx.send(f"The current confession channel is <#{confessionChannel.id}>")
        else:
          await ctx.send(f"No confession channel is currently set, Use `{prefs[str(ctx.guild.id)]['prefix']}setConfessionChannel` to assign one.")

      except ValueError:
        await ctx.send(f"Error finding channel - Please report this issue to {dev} if the issue persists")

      except Exception as e:
        await ctx.send(f"Error: {e} - Please report this issue to {dev} if the issue persists")

    else:
      await ctx.send(f"No confession channel is currently set, Use `{prefs[str(ctx.guild.id)]['prefix']}setConfessionChannel` to assign one.")

  @commands.guild_only()
  @commands.command(aliases=["delconfessionchannel","delConfessionchannel", "delconfessionChannel","remconfessionchannel","remConfessionchannel", "remconfessionChannel","remConfessionChannel", "delchannel", "delChannel"])
  @has_permissions(administrator=True)
  async def delConfessionChannel(self, ctx):

    with open(os.getcwd() + "/prefrences.json", "r") as f:
      prefs = json.load(f)

    if prefs[str(ctx.guild.id)]["confessionChannel"] != None:
      prefs[str(ctx.guild.id)]["confessionChannel"] = None

      await ctx.send("Channel removed!")

    else:
      await ctx.send(f"No confession channel is currently set, Use `{prefs[str(ctx.guild.id)]['prefix']}setConfessionChannel` to assign one.")

    with open(os.getcwd() + "/prefrences.json", "w") as f:
        json.dump(prefs, f, indent=4)


  @setConfessionChannel.error
  async def setConfessionChannel_error(ctx, error):
    print("setConfessionChannel_error(): ", error)
    if isinstance(error, commands.MissingRequiredArgument):
      await ctx.send("Please specify a channel to set")

def setup(client):
  client.add_cog(ConfessionConfig(client))
  print(f"Module '{os.path.basename(__file__)}' initialised")


