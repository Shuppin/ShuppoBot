import discord
from discord.ext import commands

import requests

import os
import asyncio
import time

import secrets

class Miscellaneous(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.command()
    async def ping(self, ctx):

        loading = self.bot.get_emoji(953217623779311616)

        starttime = time.time()

        try:
            embed=discord.Embed(description=f"{loading} Working")
            msg_start = time.time()
            message = await ctx.send(embed=embed)
            message_time = round((time.time()-msg_start)*1000)
        except:
            message_time = -1


        try:
            response = requests.get('https://discord.com/api/')
            api_time = round(response.elapsed.microseconds/1000)
        except:
            api_time = -1

        bot_latency = round(self.bot.latency*1000)

        value = [ 
            f"{self.get_status_emoji(message_time, range=[-1,400])[0]} **Discord Message Event** Delay is `{self.get_status_emoji(message_time, range=[-1,400])[1]}`\n",
            f"{self.get_status_emoji(api_time)[0]} **Discord API** Latency is `{self.get_status_emoji(api_time)[1]}`\n",
            f"{self.get_status_emoji(round(secrets.init_time*1000), range=[-1, 4500])[0]} **Server Instance Initialisation** time `{self.get_status_emoji(round(secrets.init_time*1000), range=[-1, 4500])[1]}`\n",
            "\n",
            f"{self.get_status_emoji(bot_latency)[0]} **Main Client** Latency is `{self.get_status_emoji(bot_latency)[1]}`\n",
            f"{self.get_status_emoji(round((time.time() - starttime)*1000), range=[-1,500])[0]} **End-To-End** Latency is `{self.get_status_emoji(round((time.time() - starttime)*1000), range=[-1,500])[1]}`"
        ]

        value = "".join(value)

        embed=discord.Embed(title=":ping_pong: Pong!")
        embed.add_field(name="\u200B", value=value, inline=True)
        embed.set_footer(text=f"Calculated at {time.strftime('%d-%m-%y %X')} (UTC) • {ctx.message.id}")

        await message.delete()
        await ctx.send(embed=embed)

    def get_status_emoji(self, ms, range=[-1, 250]):
        if ms <= range[0]:
            return '🔴', 'Not responding'
        elif range[0] < ms <= range[1]:
            return '🟢', str(ms) + 'ms'
        else:
            return '🟠', str(ms) + 'ms'

def setup(client):
  client.add_cog(Miscellaneous(client))
  print(f"Module '{os.path.basename(__file__)}' initialised")


message = {
  "channel_id": '',
  "content": "",
  "tts": False,
  "embeds": [
    {
      "type": "rich",
      "title": ':ping_pong: Pong!',
      "description": "",
      "color": 0x00FFFF,
      "fields": [
        {
          "name": '🟢\tBot Latency `100ms`',
          "value": "\u200B"
        }
      ]
    }
  ]
}