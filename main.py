import discord
from discord.ext import commands
import qlist
import question_embed
import asyncio
import os



TOKEN = os.getenv('token')
bot = commands.Bot(command_prefix='!')
client= discord.Client()


@bot.command()
async def respct(ctx):
    embed = discord.Embed(
      title='Respct OnBoarding Application',
      description = 'Congratulations! You are now a verified \nmember of our Discord.\n\n\nIf you want to become a member of Respct,\ngo ahead, read our white paper (link) and then take a short quiz!\n\n\nClick on the green button to start the quiz and get onboard.',
      color= 0xA020F0)
    embed.set_image(url="https://www.respct.fun/Respct_d.png")
    buttons= discord.ui.Button(label="Start",
                    style=discord.ButtonStyle.green,
                    emoji='⚡'
                  )
    buttons.callback=on_button_click
    view = discord.ui.View()
    view.add_item(buttons)
    await ctx.send(embed=embed, view=view)


@bot.event
async def on_button_click(interaction):
  pts=0
  message = interaction.message
  
  while(pts!=9):
    embed = question_embed.qe(pts+1,qlist.Ql[pts],qlist.Q1l[pts],qlist.Q2l[pts],qlist.Q3l[pts],qlist.Q4l[pts])
    await message.edit(embed=embed)
    for e in qlist.El:
      await message.add_reaction(e)

    res = await bot.wait_for('reaction_add')
    if qlist.Al[pts] in str(res.emoji):
      pts+=1
      continue
      
  endEmbed = discord.Embed(
      title='Respct OnBoarding Application',
      description = 'Thanks for participating in the Quiz, You are now a member. Please return to the server.',
      color= 0xA020F0) 

bot.run(TOKEN)

