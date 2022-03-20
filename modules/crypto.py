import discord
from discord.ext import commands

import os
import json
from io import BytesIO
import time

import requests
import numpy as np
from PIL import Image

class Crypto(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  @commands.guild_only()
  async def lookupCoin(self, ctx, *coin):

    loading = self.bot.get_emoji(953217623779311616)
    red_cross = self.bot.get_emoji(953217989237436426)

    if len(coin) < 1:
      embed=discord.Embed(title=f"{red_cross}  Please enter a currency", color=0xff0000)
      await ctx.send(embed=embed)
      return

    starttime = time.time()
    
    coin = ' '.join(coin)
    
    embed=discord.Embed(description=f"{loading} Working")
    message = await ctx.send(embed=embed)
    
    try:
      coinList = self.evalCoinGecko('https://api.coingecko.com/api/v3/coins/list')
      coins = self.evalCoinGecko(f'https://api.coingecko.com/api/v3/search?query={coin}')

      if len(coins['coins']) > 0:

        info = coins['coins'][0]

        coinInfo = self.evalCoinGecko(f"https://api.coingecko.com/api/v3/coins/{info['id']}")

        avg_colour = self.getImageMean(info['large'])

        hex_colour = '0x%02x%02x%02x' % tuple(map(lambda x: round(x), avg_colour))
        hex_colour = int(hex_colour, 0)

        endtime = time.time()
          
        description_txt = f"**Overall rank:** {coinInfo['coingecko_rank']}\n**Rank by market cap:** {coinInfo['market_cap_rank']}\n**Price (USD→{info['symbol'].upper()}):** ${'{:,}'.format(coinInfo['market_data']['current_price']['usd'])} "
        footer = f"Searched {'{:,}'.format(len(coinList))} currencies is {round((endtime-starttime)*1000,2)}ms"

        if len(coinInfo['links']['homepage']) > 1:
          embed=discord.Embed(title=f"{info['name']} ({info['symbol']})",       description=description_txt, color=hex_colour, url=coinInfo['links']['homepage'][0])
        else:
          embed=discord.Embed(title=f"{info['name']} ({info['symbol']})",       description=description_txt, color=hex_colour)

         
        embed.set_thumbnail(url=info['thumb'])
        embed.set_footer(text=footer)
        await message.delete()
        await ctx.send(embed=embed)

      else:
        await message.delete()

        endtime = time.time()
        footer = f"Searched {'{:,}'.format(len(coinList))} currencies is {round((endtime-starttime)*1000,2)}ms"
        
        embed=discord.Embed(title=f"{red_cross} Could not find currency '{coin}'", color=0xff0000)
        embed.set_footer(text=footer)
        await ctx.send(embed=embed)
      
      
    except Exception as e:
      print(e)


  def getImageMean(self, URL):
    response = requests.get(URL)
    img = Image.open(BytesIO(response.content))
    img = img.convert('RGB')
    imgNP = np.array(img)

    average = imgNP.mean(axis=0).mean(axis=0)

    return tuple(average)[:3]

  def evalCoinGecko(self, URL):
    response = requests.get(URL)
    content = response.content.decode('utf-8')
    contentDict = json.loads(content)
    return contentDict


def setup(client):
  coinGecko = requests.get('https://api.coingecko.com/api/v3/ping')
  if coinGecko.status_code == 200:
    client.add_cog(Crypto(client))
    print(f"Module '{os.path.basename(__file__)}' initialised")
  else:
    print(f"Could not load module '{os.path.basename(__file__)}', Coin gecko gave unexpected response <Response {coinGecko.status_code}>")