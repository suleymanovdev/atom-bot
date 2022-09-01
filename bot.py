# Libs
from typing import Optional
import discord
import datetime, asyncio, random, time
from pathlib import Path
import json
import contextlib
import io
import textwrap
import os
import logging

from datetime import datetime
from discord import Member
from discord.ext import commands
from discord.ext.commands.errors import BadUnionArgument
from discord.ext.commands import has_permissions, MissingPermissions
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
from colorama import Fore, Back, Style

#################### STATUS ######################################################################################################

bot = commands.Bot(command_prefix=get_prefix, intents=discord.Intents.all(), case_insensitive=True)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(message)s",
    filename="log.txt"
)                                               

def art():
    logo_list = ["	Atom {} Developers",
                 "     Discord Bot    ",
                 "	 by suleymanovdev "]
    for i in logo_list:
        print(f"{i}")
        time.sleep(0.2)

def get_prefix(bot, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

cwd = Path(__file__).parents[0]
cwd = str(cwd)
time_now = datetime.now()
SECRET_FILE = json.load(open(cwd + '/secrets.json'))
bot.config_token = SECRET_FILE['token']
bot.remove_command('help')
bot.remove_command('weather')
bot.remove_command('timer')
owm_key = SECRET_FILE['owm_key']
owm = OWM(owm_key)
mgr = owm.weather_manager()
vers_id = SECRET_FILE['id']
version = SECRET_FILE['version']
print(f"Bot Path: {cwd} .")
print(f"Start time: {time_now} .")
print(f"Ping in {bot.latency} ms.")
print(f"Version ID: {vers_id} .")
print(f"Version NAME: {version} .")

#################### STATUS ######################################################################################################

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

#################### ERROR #######################################################################################################

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

#################### COMMANDS ####################################################################################################
        
art() # Logo And Start Flag
        
@bot.command() # Bot Version
async def botvers(ctx):
    await ctx.send(f"`The bot version is {version}.`")

@bot.command()
async def help(ctx): # Bot Help Function
    emb = f"""```Attention, this is a bot created for programmers and their communities. The bot is under beta-development. Therefore, it will not work for some time.\n\n
\t;changeprefix - You can change bot prefix on your server.\n\n
\t;weather - Show weather information(owm). <;weather London>\n\n
\t;timer - Bot starting timer for you. <;timer 30>\n\n
\t;botvers - Show the bot's version. <;botvers>```"""
    await ctx.send(emb)

@bot.command()
async def timer(ctx, seconds): # Bot Timer Function
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

@bot.command()
async def weather(ctx, *, arg): # Bot Weather Function
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

@commands.has_permissions(manage_channels=True)
@bot.command()
async def changeprefix(guild, ctx, prefix): # Change Bot Prefix Function
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(ctx.guild.id)] = prefix
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    temp_guild_id = str(guild.id)
    print("[CHANGE PREFIX] GUILD: {temp_guild_id} > PREFIX: {prefix}.")

@bot.command(pass_context=True, aliases=['clean'])
@commands.has_permissions(manage_channels=True)
async def clear(ctx, amount=500): # Chat Clear Function
    await ctx.channel.purge(limit=amount)

#################### FORMS #######################################################################################################
    
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

##################################################################################################################################
        
#About
@bot.command()
async def about(ctx):
    members = len(set(bot.get_all_members()))
    emb = discord.Embed(title='Bot Information.',timestamp=ctx.message.created_at, colour=discord.Colour.from_rgb(207, 215, 255))
    emb.add_field(name='🔗 ADD ME', value='https://bit.ly/3nKUT8i')
    emb.add_field(name='🔗 WEBSITE', value='suleymanovdev.github.io/bot (Beta)')
    emb.add_field(name='🔗 SERVER', value='https://discord.gg/5Jx8rX282v')
    emb.add_field(name='✌ SERVERS', value=f'{len(bot.guilds)}')
    emb.add_field(name='✌ PARTICIPANS', value=f"{members}")
    emb.add_field(name='👑 CREATOR', value='suleymanovdev#9475')
    emb.add_field(name='🔗 GITHUB', value='https://github.com/suleymanovdev/atom-bot')
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
     👋 Hello friend, my name is **Atom Bot™**!

     😎 My creator build me for helping you.
     
     😎 My prefixes are `;`.
     😲 Write the `;help` command to find out all my options!
     📃 Do you want to know a little about me? Write `;about`!
     🤔 Need help with the bot, or found a bug/error? Come to our `Atom Discord Server`!

     👻 Good luck!
    ''')
                await message.reply(embed=emb)

#Updates
@bot.command()
async def updates(ctx):
    emb = discord.Embed(title='Bot updates.', description='Here my creator writes about my updates.',timestamp=ctx.message.created_at, colour=discord.Colour.from_rgb(207, 215, 255))
    emb.add_field(name='2.1 Fridrich', value='Settings visualization, clear & change prefix permissions.')
    await ctx.send(embed=emb)

#Start
bot.run(bot.config_token)
