# +----------------------------------+ MODULES +---------------------------------------------------------------------------------------------------------------------------------------+

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
import openai
import requests

from datetime import datetime
from discord import Member
from discord import File
from discord import app_commands
from discord.ext import commands
from discord.ext.commands.errors import BadUnionArgument
from discord.ext.commands import has_permissions, MissingPermissions
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
from bs4 import BeautifulSoup

# +----------------------------------+ SETTINGS +--------------------------------------------------------------------------------------------------------------------------------------+

bot = commands.Bot(command_prefix="/", intents=discord.Intents.all(), case_insensitive=True)
logging.basicConfig
(
    level:=logging.DEBUG,
    format:="%(asctime)s | %(levelname)s | %(message)s",
    filename:="log.txt"
)

cwd = Path(__file__).parents[0]
cwd = str(cwd)
time_now = datetime.now()
SECRET_FILE = json.load(open(cwd + '/secrets.json'))
bot.config_token = SECRET_FILE['token']
bot.remove_command('help')
bot.remove_command('weather')
bot.remove_command('timer')
owm_key = SECRET_FILE['owm_key']
openai_key = SECRET_FILE['openai_key']
owm = OWM(owm_key)
mgr = owm.weather_manager()
vers_id = SECRET_FILE['id']
version = SECRET_FILE['version']

# +------------------------------------+ STATUS +--------------------------------------------------------------------------------------------------------------------------------------+

@bot.event
async def on_ready():
    synced = await bot.tree.sync()
    os.system("clear")
    stats = f"""
        •—————————————————————————————————————•
           Bot Name: {bot.user.name}
           Bot Path: {cwd}
           Ping (ms): {bot.latency}
           Version ID: {{vers_id}
           Commands: {len(synced)}
        •—————————————————————————————————————•
	"""
    print(stats)
    await bot.change_presence(activity=discord.Game(name=f"{version} | /help | atomdg.com/bot"))

# +------------------------------------+ STATUS +--------------------------------------------------------------------------------------------------------------------------------------+

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(' :no_entry_sign:  `|`  **Sorry you dont have permission to use this command!**')
    if isinstance(error, commands.BotMissingPermissions):
        await ctx.send(' :no_entry_sign:  `|`  **Sorry you dont have permission for a bot!**')
    if isinstance(error, commands.MemberNotFound):
        await ctx.send(' :name_badge:  `|`  **This member does not exist.**')

# +------------------------------------+ COMMANDS +------------------------------------------------------------------------------------------------------------------------------------+

@bot.tree.command(name='formula1', description='Get the latest Formula 1 news') 
async def formula1(interaction: discord.Interaction):
    await interaction.response.send_message(embed=discord.Embed(title="Retrieving the latest Formula 1 news...",color=discord.Color.red()))
    response = requests.get('https://www.formula1.com/en/latest/all.html')
    soup = BeautifulSoup(response.text, 'html.parser')
    news_articles = soup.select('p.f1--s.no-margin')
    news_articles = [p.get_text().replace("â\x80\x99s", "'").replace("â", " ") for p in news_articles if p.get_text() != 'Sorry']    
    news_articles_md = '\n'.join([f'- {article}' for article in news_articles])
    news_articles = news_articles[:15]
    if news_articles_md:
        embed = discord.Embed(title="Here are the latest Formula 1 news headlines:",description=f"{news_articles_md}",color=discord.Color.red())
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/F1.svg/2560px-F1.svg.png")
        embed.set_footer(
            text="Formula 1 News: https://www.formula1.com/en/latest/all.html",
            icon_url="https://avatars.githubusercontent.com/u/109563195?s=400&u=51dcd9720783d251feccdb16a451813b04e30597&v=4"
        )
        await interaction.followup.send(embed=embed)
    else:
        await interaction.followup.send('Sorry, there was an error retrieving the latest Formula 1 news. Please try again later.')

@bot.tree.command(name='github', description='Get the latest GitHub news')
async def github(interaction: discord.Interaction):
    await interaction.response.send_message(embed=discord.Embed(title="Retrieving the latest GitHub news...",color=discord.Color.dark_grey()))
    response = requests.get('https://github.com/about/press?page=1')
    soup = BeautifulSoup(response.text, 'html.parser')
    news_articles = soup.select('h3.f3-mktg.text-normal')
    news_articles = [p.get_text().replace("â\x80\x99s", "'").replace("â", " ") for p in news_articles if p.get_text() != 'Sorry']    
    news_articles_md = '\n'.join([f'- {article}' for article in news_articles])
    news_articles = news_articles[:15]
    if news_articles_md:
        embed = discord.Embed(title="Here are the latest GitHub news headlines:",description=f"{news_articles_md}",color=discord.Color.dark_grey())
        embed.set_thumbnail(
			url="https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Octicons-mark-github.svg/2048px-Octicons-mark-github.svg.png"
			)
        embed.set_footer(
			text="GitHub News: https://github.com/about/press",
			icon_url="https://avatars.githubusercontent.com/u/109563195?s=400&u=51dcd9720783d251feccdb16a451813b04e30597&v=4"
		)
        await interaction.followup.send(embed=embed)
    else:
        await interaction.followup.send('Sorry, there was an error retrieving the latest GitHub news. Please try again later.')

@bot.tree.command(name='appledev', description='Get the latest Apple Developer news')
async def appledev(interaction: discord.Interaction):
    await interaction.response.send_message(embed=discord.Embed(title="Retrieving the latest Apple Developer news...",color=discord.Color.dark_grey()))
    response = requests.get('https://developer.apple.com/news/')
    soup = BeautifulSoup(response.text, 'html.parser')
    news_articles = soup.select('h2')
    response = requests.get('https://developer.apple.com/news/')
    soup = BeautifulSoup(response.text, 'html.parser')
    news_articles = soup.select('h2')
    news_articles = [p.get_text().replace("â\x80\x99s", "'").replace("â", " ") for p in news_articles if p.get_text() != 'News and Updates'][:15][1:]
    news_articles_md = '\n'.join([f'- {article}' for article in news_articles])
    if news_articles_md:
        embed = discord.Embed(title="Here are the latest Apple Developer news headlines:",description=f"{news_articles_md}",color=discord.Color.dark_grey())
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_first_logo.png")
        embed.set_footer(
			text="Apple Developer News: https://developer.apple.com/news/",
			icon_url="https://avatars.githubusercontent.com/u/109563195?s=400&u=51dcd9720783d251feccdb16a451813b04e30597&v=4"
		)
        await interaction.followup.send(embed=embed)
    else:
        await interaction.followup.send('Sorry, there was an error retrieving the latest Apple Developer news. Please try again later.')

@bot.tree.command(name="gpt", description='Ask ChatGPT question')
@app_commands.describe(question="Enter Your Question")
async def gpt(interaction: discord.Interaction, question: str):
    messages = [{"role": "system", "content": "You are a helper"}]
    messages.append({"role": "user", "content": question})
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        ChatGPT_reply = response["choices"][0]["message"]["content"]
        embed = discord.Embed(title="GPT's Answer:", description=response["choices"][0]["text"])
        await interaction.response.send_message(embed=embed)
    except openai.error.RateLimitError as e:
        await interaction.response.send_message("Sorry, we have exceeded the API quota. Please try again later.")
	
@bot.tree.command(name="weather", description='Get weather news')
@app_commands.describe(city_name = "Enter City Name")
async def weather(interaction: discord.Integration, city_name: str):
    observation = mgr.weather_at_place(city_name)
    w = observation.weather
    embed = discord.Embed(title=f'Weather in {city_name}:')
    embed.add_field(name='Show Status:', value=w.detailed_status)
    embed.add_field(name='Wind Info:', value=w.wind())
    embed.add_field(name='Teperature:', value=w.temperature('celsius'))
    embed.add_field(name='Cloud Percent:', value=w.clouds)
    embed.add_field(name='Humidity:', value=w.humidity)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="botvers", description='Get Bot Version')
async def botvers(interaction: discord.Integration):
    await interaction.response.send_message(f"`The bot version is {version}.`")

@bot.tree.command(name="help", description='Get Help Menu')
async def help(interaction: discord.Integration):
    embed = discord.Embed(title=f'Help Book')
    embed.add_field(name=f'/about', value='📓 Information')
    embed.add_field(name=f'/updates', value='📓 Information')
    embed.add_field(name=f'/botvers', value='📓 Information')
    embed.add_field(name=f'/weather', value='✌️ For Users')
    embed.add_field(name=f'/gpt', value='✌️ For Users')
    embed.add_field(name=f'/formula1', value='✌️ For Users')
    embed.add_field(name=f'/appledev', value='✌️ For Users')
    embed.add_field(name=f'/github', value='✌️ For Users')
    embed.add_field(name=f'/bug (your error)', value='🛠️ Developers Support')
    embed.add_field(name=f'/idea (your idea)', value='🛠️ Developers Support')
    embed.add_field(name=f'/feedback (your feedback)', value='🛠️ Developers Support')
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="bug", description='Send Bot Bug to developers')
@app_commands.describe(message = "Enter Your Error Message")
async def bug(interaction: discord.Integration, message: str):
    if message != '':
        await interaction.response.send_message("Sended!")
        chan = bot.get_channel(1088082395988754484)
        emb = discord.Embed(title='Found a bug in the bot!')
        emb.add_field(name='Description:', value=message)
        await chan.send(embed=emb)

@bot.tree.command(name="feedback", description='Send Bot Feedback to developers')
@app_commands.describe(message = "Enter Your Feedback")
async def feedback(interaction: discord.Integration, message: str):
    if message != '':
        await interaction.response.send_message("Sended!")
        chan = bot.get_channel(1088082503589449758)
        embed = discord.Embed(title='Bot feedback!')
        embed.add_field(name='Description + rating:', value=message)
        await chan.send(embed=embed)

@bot.tree.command(name="idea", description='Send Bot Idea to developers')
@app_commands.describe(message = "Enter Your Idea")
async def idea(interaction: discord.Integration, message: str):
    if message is None:
        embed = discord.Embed(title="Err", description=f"Enter your idea `/idea <idea>`",color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
    else:
        channel = await bot.fetch_channel(1088082442398744666)
        embed = discord.Embed(title="New Idea!",description=f"**Content:**\n{message}",color=discord.Color.green())
        msg = await channel.send(embed=embed)
        embed2 = discord.Embed(title="Sucs!",description=f"Idea was **successfully** submitted\n**Content:\n{message}**",color=discord.Color.green())
        await interaction.response.send_message(embed=embed2)

@bot.tree.command(name="about", description='Get Bot Information')
async def about(interaction: discord.Integration):
    members = len(set(bot.get_all_members()))
    emb = discord.Embed(title='Bot Information.', colour=discord.Colour.from_rgb(207, 215, 255))
    emb.add_field(name='🔗 ADD ME', value='https://bit.ly/atomdevelopersbot')
    emb.add_field(name='🔗 WEBSITE', value='https://atomdg.com/bot (Beta)')
    emb.add_field(name='🔗 SERVER', value='https://bit.ly/adgcommunity')
    emb.add_field(name='✌ SERVERS', value=f'{len(bot.guilds)}')
    emb.add_field(name='✌ PARTICIPANS', value=f"{members}")
    emb.add_field(name='👑 CREATOR', value='sudev#5563')
    emb.add_field(name='🔗 GITHUB', value='https://bit.ly/atombotrepo')
    await interaction.response.send_message(embed=emb)

@bot.tree.command(name="updates", description='Get Bot Updates')
async def updates(interaction: discord.Integration):
    emb = discord.Embed(title='Bot updates.', description='Here my creator writes about my updates.', colour=discord.Colour.from_rgb(207, 215, 255))
    emb.add_field(name=f'{version}', value='https://atomdg.com/bot/updates')
    await interaction.response.send_message(embed=emb)

# +------------------------------------+ BOT.RUN +-------------------------------------------------------------------------------------------------------------------------------------+

bot.run(bot.config_token)
