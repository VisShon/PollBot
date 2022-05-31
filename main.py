from pydoc import cli
import discord
from discord.ext import commands
import question_embed
import pymongo
import os

from decouple import config

TOKEN = config('token')
MongoURL = config('url')

# list of emote options
optList = ['🔶','🟥','🔷','🟩']

# connecting to bot
bot = commands.Bot(command_prefix='!',intents=discord.Intents.all())

# connecting to mongodb
Mclient = pymongo.MongoClient(MongoURL)
db = Mclient["respct"]

@bot.command(name="quiz", help="Redirect to the quiz page")
async def quiz(ctx):
  embed = discord.Embed(
        title='Respct OnBoarding Application',
        description=
        'To apply for a membership to our platform, \nDm me and take the quiz using !respct command to \nverify yourself',
        color=0xA020F0)
  embed.set_image(url="https://i.ibb.co/HqmsfNv/Mask-Group.png")
  await ctx.send(embed=embed)


@bot.command(name="respct", help="start the quiz")
async def respct(ctx):
    # generating the initial embed
    embed = discord.Embed(
        title='Respct OnBoarding Application',
        description=
        'Congratulations! You are now a verified \nmember of our Discord.\n\n\nIf you want to become a member of Respct,\ngo ahead, read our white paper (link) and then take a short quiz!\n\n\nClick on the green button to start the quiz and get onboard.\n\n',
        color=0xA020F0)
    embed.set_image(url="https://i.ibb.co/qjgb7Z5/Group-48.png")
    buttons = discord.ui.Button(label="Start",
                                style=discord.ButtonStyle.green,
                                emoji='⚡')
    buttons.callback = lambda interaction: on_button_click(interaction, buttons)
    view = discord.ui.View()
    view.add_item(buttons)
    await ctx.send(embed=embed, view=view)

@bot.command(name="status", help="Give the user status")
async def status(ctx):
  col = db["Users"]
  query={"DiscordId":"Vis.n_u#3089"}
  data =  col.find(query)

  for i in data:
    x= f'\nguild: {i["guild"]}, game: {i["game"]}, score: {i["score"]}'

  embed = discord.Embed(
        title='Respct OnBoarding Application',
        description=
        x,
        color=0xA020F0)
  await ctx.send(embed=embed)

@bot.event
async def on_button_click(interaction,button):

    user = str(interaction.user)
    channel = interaction.channel

    embed = discord.Embed(
          title='Respct OnBoarding Application',
          description=
          'Enter GuildName / GameName\nyou want to give the quiz of\n\nExample: IndieGG/AxieInfinity',
          color=0xA020F0)
    embed.set_image(url="https://cdn3d.iconscout.com/3d/premium/thumb/game-controller-4035922-3342601@0.png")
    await interaction.response.send_message(embed=embed)


    def check(m):
        return True
    msg = await bot.wait_for("message", check=check)
    arr = msg.content.split("/")
    guildName="IndieGG"
    gameName="AxieInfinity"


    embed = discord.Embed(
          title='Respct OnBoarding Application',
          description=
          'Quiz Started',
          color=0xA020F0)
    await interaction.followup.send(embed=embed)
  
    pts = 0
    n=0

    while (pts != 9):

      # fetching the quiz collection
      col = db["Quizes"]
      query={"guildName":guildName}
      data =  col.find(query)
  
      for ques in data:
        Q=ques["games"][gameName][pts]["Q"]
        op1=ques["games"][gameName][pts]["op1"]
        op2=ques["games"][gameName][pts]["op2"]
        op3=ques["games"][gameName][pts]["op3"]
        op4=ques["games"][gameName][pts]["op4"]

      embed = question_embed.qe(pts+1,Q,op1,op2,op3,op4)
      returnVal = await channel.send(embed=embed)

      # generating options from
      for e in optList:
        await returnVal.add_reaction(e)

      answered = False
      playerInput = None

      # listner for response
      while not answered:
        returnVal = await returnVal.edit(embed=embed)
        for x in returnVal.reactions:
          if x.count == 2:
            answered = True
            playerInput = x

      # check for correct answer
      if str(playerInput.emoji) == ques["games"][gameName][pts]["ans"]:
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
    data={"DiscordId":user,"guild":guildName,"game":gameName,"score":n}
    col.insert_one(data)

    if(n>4):
      await channel.send(embed=endEmbedPass)
    else:
      await channel.send(embed=endEmbedFail)


bot.run(TOKEN)
