from sys import executable
import discord
from discord.ext import commands
import youtube_dl
import os
import urllib.parse, urllib.request, re
import requests
import Constants

class music(commands.Cog):
    def __init__(self, client):
        self.client = client

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
        await ctx.send("Now playing " + videoTitle + " at " + url3)

        await self.play(ctx, url3)


# Disconnect Command
    @commands.command()
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()
    
# The Actual Music Playing
    @commands.command()
    async def play(self, ctx, url):
        ctx.voice_client.stop()
        FFMPEG_OPTIONS = {"before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", "options": "-vn"}
        YDL_OPTIONS = {"format" : "bestaudio"}
        vc = ctx.voice_client

        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download = False)
            url2 = info["formats"][0]["url"]
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS, executable=os.path.join(os.path.dirname(__file__), "ffmpeg/bin/ffmpeg.exe"))
            vc.play(source)
    
# Pause Command
    @commands.command()
    async def pause(self, ctx):
        await ctx.voice_client.pause()
        await ctx.send("Music paused")

# Resume Command
    @commands.command()
    async def resume(self, ctx):
        await ctx.voice_client.resume()
        await ctx.send("Music resumed")
    

def setup(client):
    client.add_cog(music(client))