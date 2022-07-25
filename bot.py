# Libs
from typing import Optional
import discord
import datetime, asyncio, random
from pathlib import Path
import json
import contextlib
import io
import textwrap
import os
import calendar
import logging

from datetime import datetime
from discord import Member
from discord.ext import commands
from discord.ext.commands.errors import BadUnionArgument
from discord.ext.commands import has_permissions, MissingPermissions
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps

#Setup
def clear():
    os.system("clear")

def get_prefix(bot, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

bot = commands.Bot(command_prefix=get_prefix, intents=discord.Intents.all(), case_insensitive=True)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(message)s",
    filename="log.txt"
)                                               

import time
def art():
    logo_list = ["	Atom {} Developers",
                "		    Discord Bot   ",
                "		    Python Code   "]
    for i in logo_list:
        print(f"{i}")
        time.sleep(0.2)
art()
cwd = Path(__file__).parents[0]
cwd = str(cwd)
time_now = datetime.now()
print(f"Bot Path: {cwd} .")
print(f"Start time: {time_now} .")
print(f'Ping in {bot.latency} ms.')


#Setup for bot run && bot prefix && owm settings
version = '1.0 Dyric'
secret_file = json.load(open(cwd + '/secrets.json'))
bot.config_token = secret_file['token']
bot.remove_command('help')
owm_key = '612ad9194bbdf063190cdfe5813f246c'
owm = OWM(owm_key)
mgr = owm.weather_manager()


#Setup for bot status
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=f";help | {version}"))


@bot.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = ';'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@bot.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

#Errors in chat
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(' :no_entry_sign:  `|`  **Sorry you dont have permission to use this command!**')
    if isinstance(error, commands.BotMissingPermissions):
        await ctx.send(' :no_entry_sign:  `|`  **Sorry you dont have permission for a bot!**')
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(' :name_badge:  `|`  **This command does not exist, write `;help`.**')
    if isinstance(error, commands.MemberNotFound):
        await ctx.send(' :name_badge:  `|`  **This member does not exist.**')
    if isinstance(error, commands.BadArgument):
        await ctx.send(' :name_badge:  `|`  **Wrong argument.**')


#Version
@bot.command()
async def botvers(ctx):
    await ctx.send(f"`The bot version is {version}.`")


#Help
@bot.command()
async def help(ctx):
    emb = f"""```Attention, this is a bot created for programmers and their communities. The bot is under beta-development. Therefore, it will not work for some time.\n\n
\t;sds - About SuleymanovDev server.\n\n
\t;changeprefix - You can change bot prefix on your server.\n\n
\t;weather - Show weather information(owm). <;weather London>\n\n
\t;timer - Bot starting timer for you. <;timer 30>\n\n
\t;botvers - Show the bot's version. <;botvers>```"""
    await ctx.send(emb)


#SDS
@bot.command()
async def sds(ctx):
    await ctx.send("`SD✌️ is a community of programmers created by suleymanovdev#9475 ,where you can share various interesting news from the world of information technology. Share codes, discuss codes of other participants. Become one of the coolest programmers.We are committed to ensuring that everyone learns and starts writing code at a professional level.`")

#Timer
@bot.command()
async def timer(ctx, seconds):
    try:
        secondint = int(seconds)
        if secondint > 3600:
            await ctx.send("```I can't go over 1 hour :(```")
        if secondint <= 0:
            await ctx.send("```I can't do negatives...... -_-```")
        message = await ctx.send(f"Timer: {seconds}")
        while True:
            secondint -= 1
            if secondint == 0:
                await message.edit(content="```Ended!```")
                break
            await message.edit(content=f"```Timer: {secondint}```")
            await asyncio.sleep(1)
        await ctx.send(f"{ctx.author.mention}```, Your timer has been ended! (Thank you for using suleymanovdev Bot in your life :3```")
    except ValueError:
        await ctx.send("***ValueError:*** **You must enter number!, if it doesn't work write** ```<bot prefix>bug``` **command.**")

#Weather
@bot.command()
async def weather(ctx, *, arg):
    if arg != '':
        city_input = arg
        observation = mgr.weather_at_place(city_input)
        w = observation.weather
        embed = discord.Embed(title=f'Weather in {city_input}:')
        embed.add_field(name='Show Status:', value=w.detailed_status)
        embed.add_field(name='Wind Info:', value=w.wind())
        embed.add_field(name='Teperature:', value=w.temperature('celsius'))
        embed.add_field(name='Cloud Percent:', value=w.clouds)
        embed.add_field(name='Humidity:', value=w.humidity)
        await ctx.send(embed=embed)

#Calendar
@bot.command()
async def calendar(ctx, *, month_arg):
    a = 0
    if month_arg == "January":
        a = 1
    elif month_arg == "February":
        a = 2
    elif month_arg == "March":
        a = 3
    elif month_arg == "April":
        a = 4
    elif month_arg == "May":
        a = 5
    elif month_arg == "June":
        a = 6
    elif month_arg == "July":
        a = 7
    elif month_arg == "August":
        a = 8
    elif month_arg == "September":
        a = 9
    elif month_arg == "October":
        a = 10
    elif month_arg == "November":
        a = 11
    elif month_arg == "December":
        a = 12
    else:
        a = 1

    await ctx.send(calendar.month(2022, a))   

#Change prefix command
@bot.command()
async def changeprefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

#Clear
@bot.command(pass_context=True, aliases=['clean'])
@commands.has_permissions(manage_channels=True)
async def clear(ctx, amount=500):
    await ctx.channel.purge(limit=amount)

#Developer Program
@bot.command()
async def iamdeveloper(ctx, *, arg):
    if arg != '':
        await ctx.send("Sended!")
        chan = bot.get_channel(994335943479799891)
    emb = discord.Embed(title='Developer Program!')
    emb.add_field(name='Description:', value=arg)
    emb.add_field(name='Developer:', value=ctx.author.mention)
    await chan.send(embed=emb)
    
#Bug
@bot.command()
async def bug(ctx, *, arg):
    if arg != '':
        await ctx.send("Sended!")
        chan = bot.get_channel(994335992515395614)
    emb = discord.Embed(title='Found a bug in the bot!')
    emb.add_field(name='Description:', value=arg)
    emb.add_field(name='Bug author:', value=ctx.author.mention)
    await chan.send(embed=emb)

#Feedback
@bot.command()
async def feedback(ctx, *, arg):
    if arg != '':
        await ctx.send("Sended!")
        chan = bot.get_channel(994336055908106300)
        embed = discord.Embed(title='Bot feedback')
        embed.add_field(name='Description + rating:', value=arg)
        embed.add_field(name='Reviewer:', value=ctx.author.mention)
        await chan.send(embed=embed)

#Idea
@bot.command()
async def idea(ctx, *, idea=None):
    if idea is None:
        embed = discord.Embed(title="Err", description=f"Enter your idea `{ctx.prefix}idea <idea>`",color=discord.Color.red())
        await ctx.send(embed=embed)
    else:
        channel = await bot.fetch_channel(994336027466551327)
        embed = discord.Embed(title="New Idea!",description=f"**Sender:\n**{ctx.author.mention}\n**ID:**\n{ctx.author.id}\n**Idea:**\n{idea}",color=discord.Color.green())
        msg = await channel.send(embed=embed)
        embed2 = discord.Embed(title="Sucs!",description=f"Idea was **successfully** submitted to the channel <#808749943942283315>\n**Content:\n{idea}**",color=discord.Color.green())
        await ctx.send(embed=embed2)

#About
@bot.command()
async def about(ctx):
    members = len(set(bot.get_all_members()))
    emb = discord.Embed(title='Bot Information.',timestamp=ctx.message.created_at, colour=discord.Colour.from_rgb(207, 215, 255))
    emb.add_field(name='Add to server', value='https://bit.ly/3nKUT8i')
    emb.add_field(name='Bot website', value='suleymanovdev.github.io/bot (Beta)')
    emb.add_field(name='Bot server', value='https://discord.gg/5Jx8rX282v')
    emb.add_field(name='Number of servers', value=f'{len(bot.guilds)}')
    emb.add_field(name='Number of participants', value=f"{members}")
    emb.add_field(name='Root', value='suleymanovdev#9475')
    emb.add_field(name='GitHub', value='https://github.com/suleymanovdev')
    await ctx.send(embed=emb)

#Bot Ping
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    splited = message.content.split(' ')
    if message.author.bot is False:
        if f'<@!807249504968638494>' in splited[0]:
            try:
                if splited[1] is None:
                    pass
                else:
                    pass
            except:
                emb = discord.Embed(title=f'{message.author.display_name}!', description=f'''
     👋 Hello friend, my name is **SuleymanovDev Bot™**!

     😎 My prefixes are `;`.
     😲 Write the `;help` command to find out all my options!
     📃 Do you want to know a little about me? Write `;about`!
     🤔 Need help with the bot, or found a bug/error? Come to our `SuleymanovDev Discord Server`!

     🍀 Good luck!
    ''')
                await message.reply(embed=emb)

#Updates
@bot.command()
async def updates(ctx):
    emb = discord.Embed(title='Bot updates.', description='Here my creator writes about my updates.',timestamp=ctx.message.created_at, colour=discord.Colour.from_rgb(207, 215, 255))
    emb.add_field(
        name='-')
    await ctx.send(embed=emb)

#Start
bot.run(bot.config_token)
