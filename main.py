import discord
from discord.ext import commands
import booomBot
import os
import Constants
import platform



cogs = [booomBot]

client = commands.Bot(command_prefix="?", intents = discord.Intents.all())

@client.event
async def on_ready():    
    ## check if the file named "restart.txt" is present in the directory
    if os.path.isfile('restart.txt'):
        #if the file is present, read the first line from the file
        f = open('restart.txt', 'r')
        lines = f.readlines()
        for line in lines:
            channelId = line
        await client.get_channel(int(channelId)).send('Bot is online!')
        f.close()
        os.remove('restart.txt')
    print('Bot is online!')
    print('Logged in as ' + client.user.name)
    print("Discord.py API version:", discord.__version__)
    print("Python version:", platform.python_version())
    print("Running on:", platform.system(), platform.release(), "(" + os.name + ")")
    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXX')


for i in range(len(cogs)):
    cogs[i].setup(client)

key = 'booomBot_key'

client.run(Constants.booomBot_key)