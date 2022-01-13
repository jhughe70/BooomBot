import queue
from re import search
from sys import executable
import discord
from discord import player
from discord.ext import commands
import youtube_dl
from datetime import datetime, timezone, timedelta, time, date
import os
import urllib.request
import requests
import Constants
from queue import Queue
import itertools
from async_timeout import timeout
import asyncio



playing = False


class music(commands.Cog):
    
    def __init__(self, client):
        self.client = client


    @commands.command()
    async def reboot(self, ctx):
        ## write the channel id of the context to a file named "restart.txt"
        with open("restart.txt", "w") as f:
            f.write(str(ctx.channel.id))
        await ctx.send("Restarting...")
        try:
            await self.client.logout()
        except:
            pass
        print("Trying to reboot")
        os.system(".\.venv\Scripts\python.exe main.py")



# Join Command
    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("You must be connected to a voice channel before listening to music.")
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

# Search By Title
    @commands.command()
    async def p(self, ctx, *, search):

        htmlRequest = requests.get("https://youtube.googleapis.com/youtube/v3/search?part=snippet&q=" + search + "&type=video&maxResults=1&key=" + Constants.youtube_API)
    
        requestJSON = htmlRequest.json()
        videoID = requestJSON["items"][0]["id"]["videoId"]
        videoTitle = requestJSON["items"][0]["snippet"]["title"]

        url3 = "http://youtube.com/watch?v="+ videoID
        #await ctx.send("Now playing " + videoTitle + " at " + url3)
        

        await self.play(ctx, url3)
            

# Disconnect Command
    @commands.command()
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()
        # Clear the contents in the queue file each time the bot is disconnected
        with open("queue.txt", "r+") as f:
            f.truncate(0)
    
# The Actual Music Playing
    @commands.command()
    async def play(self, ctx, url):
        await self.join(ctx)
        #ctx.voice_client.stop()
        FFMPEG_OPTIONS = {"before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", "options": "-vn"}
        YDL_OPTIONS = {"format" : "bestaudio"}
        vc = ctx.voice_client
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download = False)
                url2 = info["formats"][0]["url"]
                print(info)
                source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS, executable=os.path.join(os.path.dirname(__file__), "ffmpeg/bin/ffmpeg.exe"))
                
                # Determine if bot is already playing audio in order to add song to queue or play immediately
                if vc.is_playing():

                    queueFile = open("queue.txt", "a")
                    queueFile.write(url + "\n")
                    queueFile.close()
                    musicEmbed = discord.Embed(title="💽 Adding To Queue 🎵", description= str(info["title"]), colour=0x005865F2)
                    musicEmbed.set_thumbnail(url=str(info["thumbnail"]))
                    musicEmbed.add_field(name= "Requested by", value= ctx.author.mention, inline=True)
                    musicEmbed.add_field(name= "Duration", value= timedelta(seconds=int(str(info["duration"]))), inline=True)
                    await ctx.send(embed=musicEmbed)



                # If nothing is currently being played, play the song that was queued
                else:
                    musicEmbed = discord.Embed(title="💽 Now Playing 🎵", description= str(info["title"]), colour=0x005865F2)
                    musicEmbed.set_thumbnail(url=str(info["thumbnail"]))
                    musicEmbed.add_field(name= "Requested by", value= ctx.author.mention, inline=True)
                    musicEmbed.add_field(name= "Duration", value= timedelta(seconds=int(str(info["duration"]))), inline=True)
                    await ctx.send(embed=musicEmbed)
                    
                    vc.play(source)
                    await asyncio.sleep(int(info["duration"]) + 2)
                    print("Finished playing.")
                    await self.serveQueue(ctx)
        return

# Queue Function                
    async def serveQueue(self, ctx):
        queueFile = open("queue.txt", "r")
        line = queueFile.readline()
        with open('queue.txt', 'r') as fin:
            data = fin.read().splitlines(True)
        with open('queue.txt', 'w') as fout:
            fout.writelines(data[1:])
        print("starting next song")
        await ctx.send("Playing next song:")
        await self.play(ctx, line)





# # Skip Command
#     @commands.command()
#     async def skip(self, ctx):
#         vc = ctx.voice_client

#         if vc.ispaused():
#             pass
#         elif not vc.is_playing():
#             await self.play
#             return
        
#         vc.stop()

# Pause Command
    @commands.command()
    async def pause(self, ctx):
        await ctx.send("Music paused")
        await ctx.voice_client.pause()

# Resume Command
    @commands.command()
    async def resume(self, ctx):
        await ctx.send("Music resumed")
        await ctx.voice_client.resume()

# Help Command To Print Viable Commands To The User
    @commands.command()
    async def booomhelp(self, ctx):
        await ctx.send("Here are a list of commmands:\n\n?play: Plays audio from YouTube using a direct url\n\n?p: Use to search a song by title (must be available on YouTube)"
        "\n\n?pause: Pauses audio\n\n?resume: Resumes audio\n\n?disconnect: Removes BooomBot from channel")
    

def setup(client):
    client.add_cog(music(client))