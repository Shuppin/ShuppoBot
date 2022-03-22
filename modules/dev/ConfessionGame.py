import discord as discord
from discord.ext import commands

import os
import json
import asyncio
from datetime import datetime

class ConfessionGame(commands.Cog):
  
  def __init__(self, bot):
    self.bot = bot
    self.active = False

  def isvalid(self, channel_id):
    with open(os.getcwd() + "/prefrences.json", "r") as f:
      prefs = json.load(f)

    print(type(self.bot.get_channel(channel_id)))

    if type(self.bot.get_channel(channel_id)) == discord.channel.TextChannel:
        return True

    else:
      return False

  def addconfession(self, server_id: str, confession: dict):

    with open(os.getcwd() + "/prefrences.json", "r") as f:
      prefs = json.load(f)

    keys = ['author_id', 'author_name', 'message', 'time']

    try:
      for key in keys:
        confession[key]
    except KeyError:
      return False, "Dictionary structure invalid"

    confession = { key: confession[key] for key in keys }

    try:
      server = prefs[str(server_id)]
      print("Server:", server)
      del server
    except KeyError as e:
      print(e)
      return False, "Could not find server"
    except Exception as e:
      print(e)
      return False, "Failed, line 52: " + e


    print("line 56, confession:", confession)

    try:
      confessions = prefs[str(server_id)]['confessions']
      print(f"line 60, prefs[{str(server_id)}]: ", prefs[str(server_id)])
    except KeyError:
      prefs[str(server_id)]['confessions'] = []
      confessions = []
    except Exception as e:
      print(e)

    confessions.append(confession)

    print("Confession:", confession)

    prefs[str(server_id)]['confessions'] = confessions

    print("Prefs:", prefs)

    with open(os.getcwd() + "/prefrences.json", "w") as f:
      print(f"Wrote {str(server_id)}:{prefs[str(server_id)]} to file")
      json.dump(prefs, f, indent=4)
      pass

    return True, "Success!"

  @commands.dm_only()
  @commands.command()
  async def confess(self, ctx):

    if self.active == False:

      self.active = True

      def check(m):
        return m.content is not None and m.channel == ctx.channel

      with open(os.getcwd() + "/prefrences.json", "r") as f:
        prefs = json.load(f)
    
      await ctx.send("Creating confession")

      mutuals = ctx.author.mutual_guilds
      mutualServers = []
      mutualNamesLowered = []
      message = ""

      for guild in mutuals:
        if self.isvalid(prefs[str(guild.id)]['confessionChannel']):
            mutualServers.append(guild)
            mutualNamesLowered.append(guild.name.lower())
            message += f"`{guild.name}`\n"

      if len(mutualServers) == 0:
        await ctx.send("No (valid) mutual servers found...")#
        self.active = False
        return

      embed=discord.Embed(title="❓ Which server do you want to send to?", description=message + "Please provide the name of the server that you would like to submit your confession to\nServer not here? Make sure the server you're trying to submit has a confession channel setup", color=0xd95757)
      await ctx.send(embed=embed)

      await asyncio.sleep(0.1)

      serverResponse = await self.bot.wait_for("message", check=check)

      if serverResponse.content.lower() in mutualNamesLowered:

        for i, server in enumerate(mutualNamesLowered):
          if serverResponse.content.lower() == server:
            server_id = mutualServers[i].id

        embed=discord.Embed(title="💬 Enter your confession", description="Please enter the confession you would like to send below.\n\nThis will be published to the server you selected for people to guess.", color=0xd95757)
        await ctx.send(embed=embed)

        await asyncio.sleep(0.1)

        confession = await self.bot.wait_for("message", check=check)

        embed=discord.Embed(title="📝 Confession Details", description=f"You are about to submit a confession.\nPlease make sure all the details are correct before submitting.\n\n**Server:** {serverResponse.content}\n\n**Confession:** '{confession.content}'\n\n**Reply with `yes/no` if you want to submit the confession.**", color=0xd95757)

        await ctx.send(embed=embed)

        await asyncio.sleep(0.1)

        submitResponse = await self.bot.wait_for("message", check=check)

        if submitResponse.content.lower() == "yes": 
          embed=discord.Embed(title="✅ Confession submitted", description="Confession successfully submitted", color=0xd95757)
          await ctx.send(embed=embed)
          print("line 118")

          dt_string = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

          print("line 122, dt_string:", dt_string)

          confessionDict = {'author_id': str(ctx.author.id), 'author_name': str(ctx.author.name), 'message': confession.content,'time': dt_string}

          print('line 126, server_id:', server_id,"\nconfessionDict: " ,confessionDict)

          try:
            state, response = self.addconfession(server_id, confessionDict)

          except Exception as e:
            state, response = False, "Failed" + e
            print(e)

          print('line 130, state, response:', state, response)

        elif submitResponse.content.lower() == "no":

          embed=discord.Embed(title="🛑 Submission Aborted", description="Please submit another response if you would like to confess.", color=0xd95757)
          await ctx.send(embed=embed)

        else:
          embed=discord.Embed(title="⚠️ Whoops!", description=f"Unrecognised response.\nPlease submit another response if you would like to confess.", color=0xd95757)
          await ctx.send(embed=embed)

      else:

        embed=discord.Embed(title="⚠️ Whoops!", description=f"Could not find server '{serverResponse.content}'.\nMake sure the spelling is correct and try again.", color=0xd95757)
        await ctx.send(embed=embed)
        confession = None
        
        self.active = False
        return

      self.active = False

def setup(client):
  client.add_cog(ConfessionGame(client))
  print(f"Module '{os.path.basename(__file__)}' initialised")

# To fix:
#   in isvalid() change self.bot.get_channel() into a server specific reference