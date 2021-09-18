import discord
from discord.ext import commands
import booomBot
import os
import Constants


cogs = [booomBot]

client = commands.Bot(command_prefix="?", intents = discord.Intents.all())

for i in range(len(cogs)):
    cogs[i].setup(client)

key = 'booomBot_key'
#print(os.environ)
print(Constants.booomBot_key)
#print(os.getenv(key))


#client.run(os.getenv(key))