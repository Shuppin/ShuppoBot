from discord.ext import commands
from discord.ext.commands import has_permissions
import os

class Moderation(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.guild_only()
  @commands.command()
  @has_permissions(administrator=True)
  async def purge(self, ctx, amount):
    
    pass

def setup(client):
  client.add_cog(Moderation(client))
  print(f"Module '{os.path.basename(__file__)}' initialised")