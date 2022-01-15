import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

import asyncio
import json
import os

class Utility(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    print("Module 'Utiliy' initialised")

  @commands.guild_only()
  @commands.command()
  async def ping(self, ctx):

    responses = []

    for i in range(4):
      responses.append(self.bot.latency*1000)
      await asyncio.sleep(0.1)

    await ctx.send(f"Pong!\nResponse times: Minimum = {round(min(responses),3)}ms, Maximum= {round(max(responses),3)}ms, Average={round(sum(responses)/len(responses),3)}ms")


  @commands.guild_only()
  @commands.command(aliases=["changePrefix", "setprefix", "setPrefix"])
  @has_permissions(administrator=True)
  async def changeprefix(self, ctx, prefix):

    if isinstance(prefix, str):

      with open(os.getcwd() + "/prefrences.json", "r") as f:
        prefs = json.load(f)
        
      prefs[str(ctx.guild.id)]['prefix'] = prefix
      await ctx.send("Prefix changed to " + prefix)

      with open(os.getcwd() + "/prefrences.json", "w") as f:
        json.dump(prefs, f, indent=4)

    else:
      await ctx.send("Invalid prefix, make sure your prefix is a string")

  @changeprefix.error
  async def changeprefix_error(self, ctx, error):
    if isinstance(error, commands.CheckFailure):
      await ctx.send("Missing permission 'Administrator'")

def setup(client):
  client.add_cog(Utility(client))