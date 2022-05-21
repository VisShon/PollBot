import discord
from discord.ext import commands
import qlist
import question_embed
import asyncio
import os
import time

TOKEN = os.getenv('token')
bot = commands.Bot(command_prefix='!')
client = discord.Client()


@bot.command()
async def respct(ctx):
    embed = discord.Embed(
        title='Respct OnBoarding Application',
        description=
        'Congratulations! You are now a verified \nmember of our Discord.\n\n\nIf you want to become a member of Respct,\ngo ahead, read our white paper (link) and then take a short quiz!\n\n\nClick on the green button to start the quiz and get onboard.',
        color=0xA020F0)
    embed.set_image(url="https://www.respct.fun/Respct_d.png")
    buttons = discord.ui.Button(label="Start",
                                style=discord.ButtonStyle.green,
                                emoji='⚡')
    buttons.callback = lambda interaction: on_button_click(interaction, buttons)
    view = discord.ui.View()
    view.add_item(buttons)
    await ctx.send(embed=embed, view=view)


@bot.event
async def on_button_click(interaction, button):

  
    embed = discord.Embed(
          title='Respct OnBoarding Application',
          description=
          'Quiz Started',
          color=0xA020F0)

  
    await interaction.response.send_message(embed=embed)
  
    pts = 0
    channel = interaction.channel
    message = interaction.message

  
    while (pts != 9):
  
      embed = question_embed.qe(pts + 1, qlist.Ql[pts], qlist.Q1l[pts],
                                qlist.Q2l[pts], qlist.Q3l[pts],
                                qlist.Q4l[pts])

      returnVal = await channel.send(embed=embed)

      for e in qlist.El:
        await returnVal.add_reaction(e)


      

      answered = False
      playerInput = None

      while not answered:
        returnVal = await returnVal.edit(embed=embed)
        for x in returnVal.reactions:
          if x.count == 2:
            answered = True
            playerInput = x
      if str(playerInput.emoji) == qlist.Al[pts]:
        pts += 1

    endEmbed = discord.Embed(
        title='Respct OnBoarding Application',
        description=
        'Thanks for participating in the Quiz, You are now a member. Please return to the server.',
        color=0xA020F0)
    await channel.send(embed=endEmbed)


bot.run(TOKEN)
