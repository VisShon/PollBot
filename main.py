from pydoc import cli
import discord
from discord.ext import commands
import question_embed
import pymongo
# import qlist
# import asyncio
# import time
# TOKEN = os.getenv('token')

optList = ['🔶','🟥','🔷','🟩']

bot = commands.Bot(command_prefix='!')
client = discord.Client()

Mclient = pymongo.MongoClient("mongodb://localhost:27017/")
db = Mclient["respct"]


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
    user = interaction.user.
    embed = discord.Embed(
          title='Respct OnBoarding Application',
          description=
          'Quiz Started',
          color=0xA020F0)

  
    await interaction.response.send_message(embed=embed)
  
    pts = 0
    n=0
    channel = interaction.channel
    message = interaction.message

    col = db["Quizes"]
    query={"guildName":"IndieGG"}
    data =  col.find(query)

    while (pts != 9):
  
      
      for ques in data:
        Q=ques["games"]["AxieInfinity"][pts]["Q"]
        op1=ques["games"]["AxieInfinity"][pts]["op1"]
        op2=ques["games"]["AxieInfinity"][pts]["op2"]
        op3=ques["games"]["AxieInfinity"][pts]["op3"]
        op4=ques["games"]["AxieInfinity"][pts]["op4"]
      embed = question_embed.qe(pts+1,Q,op1,op2,op3,op4)

      returnVal = await channel.send(embed=embed)

      for e in optList:
        await returnVal.add_reaction(e)

      answered = False
      playerInput = None

      while not answered:
        returnVal = await returnVal.edit(embed=embed)
        for x in returnVal.reactions:
          if x.count == 2:
            answered = True
            playerInput = x
      if str(playerInput.emoji) == ques["games"]["AxieInfinity"][pts]["ans"]:
        n+=1
      pts += 1

    endEmbedPass = discord.Embed(
        title='Respct OnBoarding Application',
        description=
        'Thanks for participating in the Quiz, You are now a member 😀. Please return to the server.',
        color=0xA020F0)
    endEmbedFail=discord.Embed(
        title='Respct OnBoarding Application',
        description=
        'You Failed 😭 .Thanks for participating in the Quiz and be sure to Try again',
        color=0xA020F0)

    col = db["Users"] 
    data={"DiscordId":user,"guild":"IndieGG","game":"AxieInfinity","score":n}
    col.insert_one(data)

    if(n>4):
      await channel.send(embed=endEmbedPass)
    else:
      await channel.send(embed=endEmbedFail)



bot.run('OTc2OTQ3NzcwMjE4OTMwMTk2.G1puY2.X6GYkajOvC562QkA0b-FXbUuNR7NMdhKi7-mi8')
