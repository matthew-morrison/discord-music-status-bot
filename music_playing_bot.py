from discord.ext import commands
import discord
import json
import os, time, datetime, requests, codecs
import urllib.parse
from bs4 import BeautifulSoup
import asyncio

bot = commands.Bot(command_prefix='~', description="librarian", pm_help=None, self_bot=True)


configFile = "config.json"
if os.path.isfile("config.json"):
    file = open("config.json")
    conf = json.load(file)
    discord_token = conf["discord_user_token"]
else:
    print("no config found... exploding now...")
 
async def looptons():
    while True:
        await updateSong()
        await asyncio.sleep(3)
    
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    main_loop = asyncio.get_event_loop()
    main_loop.create_task(looptons())
    
async def updateSong():
    try:
        s = requests.Session()
        s.auth = ('','1234') #shhh I know it's insecure
        r = s.get('http://localhost:8080/requests/status.xml', verify=False)
        if ('401 Client error' in r.text):
            print("web interface error, do passwords match?")
            return
    except:
        print("web interface error: is VLC running? is web interface enabled?")
        return
    artist = ""
    song = ""
    soup = BeautifulSoup(r.content, 'lxml')
    #print(soup.information)
    infos = soup.find_all("info")
    for s in infos:
        if s.attrs['name'] == 'artist':
            artist = s.contents[0]
        if s.attrs['name'] == 'title':
            song = s.contents[0]
            
    nowplaying = artist + ": "+song        
    print(nowplaying)
    await bot.change_presence(game = discord.Game(name=nowplaying))
    
    
@bot.event
async def on_message(message):   
    await bot.process_commands(message) # to the superclass ???
    
bot.run(discord_token, bot=False)
