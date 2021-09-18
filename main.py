import discord
from discord.ext import commands
import booomBot


cogs = [booomBot]

client = commands.Bot(command_prefix="?", intents = discord.Intents.all())

for i in range(len(cogs)):
    cogs[i].setup(client)

client.run("ODg4NDkyNTg0NjE0Mzc5NTUy.YUTfMw.biUtiR8ZUDfCnkGyBjGzsNQwt6o")