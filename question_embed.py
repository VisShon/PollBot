import discord
from discord.ext import commands
import asyncio

def qe(i,q,o1,o2,o3,o4):
  embed = discord.Embed(
    title=f'Q{i}/9 {q}',
    description = f':large_orange_diamond: - {o1}\n\n:red_square: - {o2}\n\n:large_blue_diamond: - {o3}\n\n:green_square: - {o4}',
    color= 0x00000
  )
  return embed