from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.commands import slash_command
import discord

import asyncio
import json
import os

from errors import InvalidMessageError


class Utility(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  async def nothing(self):
    pass


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

  @commands.guild_only()
  @commands.command()
  async def embedTest(self, ctx):
    embed=discord.Embed()
    embed.add_field(name="single \`", value="`hello`", inline=False)
    embed.add_field(name="single \` lines", value="`hello\nhello`", inline=True)
    embed.add_field(name="double \`\`", value="``hello``", inline=True)
    embed.add_field(name="double \`\` lines", value="``hello\nhello``", inline=True)
    embed.add_field(name="triple \`\`\`", value="```hello```", inline=True)
    embed.add_field(name="triple \`\`\` line", value="```hello\nhello```", inline=True)
    await ctx.send(embed=embed)


  @commands.guild_only()
  @commands.command()
  async def sendMessage(self, ctx, channelArg: str, *msg):

    if type(discord.utils.get(ctx.guild.channels, name=channelArg)) == discord.channel.TextChannel:
      channel = discord.utils.get(ctx.guild.channels, name=channelArg)

    else:
      try:

        channelArg = int(channelArg)

        if type(self.bot.get_channel(channelArg)) == discord.channel.TextChannel:

          channel = self.bot.get_channel(channelArg)

        else:
          raise Exception

      except Exception:
        await ctx.send(f"Could not find channel '{channelArg}' ")


  @commands.guild_only()
  @commands.command()
  async def print_raw(self, ctx, id: str, channel: discord.TextChannel = None):

    if channel == None:
      channel = ctx.message.channel

    msg = await channel.fetch_message(id)

    print(msg.content) # Prints an empty string
    print(msg.embeds)

  @commands.command()
  async def stats(self, ctx):
    # no of servers
    # no of users
    # pycord ver
    # python ver
    # uptime
    # owner
    pass

  @changeprefix.error
  async def changeprefix_error(self, ctx, error):
    if isinstance(error, commands.errors.NoPrivateMessage):
      return
    if isinstance(error, commands.CheckFailure):
      await ctx.send("Missing permission 'Administrator'")

  @print_raw.error
  async def print_raw_error(self, ctx, error):
    if isinstance(error, commands.errors.ChannelNotFound):
      red_cross = self.bot.get_emoji(953217989237436426)
      embed=discord.Embed(description=f"{red_cross} **Error:** {str(error)}", color=0xff0000)
      await ctx.send(embed=embed)
      return

    if isinstance(error, commands.errors.MissingRequiredArgument):
      red_cross = self.bot.get_emoji(953217989237436426)
      embed=discord.Embed(description=f"{red_cross} **Error:** Missing required argument `msg_id`", color=0xff0000)
      await ctx.send(embed=embed)
      return

    print(type(error), error)

  @slash_command()
  async def hi(self, ctx):
    await ctx.respond("Hi, this is a global slash command from a cog!")

def setup(client):
  client.add_cog(Utility(client))
  print(f"Module '{os.path.basename(__file__)}' initialised")