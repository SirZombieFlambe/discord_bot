import asyncio

import yt_dlp
from playsound import playsound
import discord
import spotdl
import spotify_dl.spotify
import vlc
from pafy import pafy
from pytube import YouTube
from yt_dlp import YoutubeDL
import ffmpeg
from youtube_dl import YoutubeDL
from moviepy.video.io.VideoFileClip import VideoFileClip
import time


class audio_cog():

    def __init__(self, api_credentials=None):

        # all the music related stuff
        self.voice = None
        self.is_playing = False
        self.is_paused = False

        # 2d array containing [song, channel]
        self.music_queue = []
        self.YDL_OPTIONS = {
                'format': 'bestaudio/best',
                'quiet': True,
            }
        self.FFMPEG_OPTIONS = {
                'options': '-vn',
                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -analyzeduration 0 -loglevel panic'
            }
        self.is_connected = False
        self.vc = None
        self.voice_client = None
        self.guild = None
        self.FFMPEG_EXECUTABLE = "D:/RandomDownload/ffmpeg.exe"

    def get_vc(self):
        return self.vc

    async def play_music(self):

        if len(self.music_queue) > 0:
            self.is_playing = True

            print("in play music")

            song = str(self.music_queue[0])

            print(song)

            if not self.is_connected:
                print("In connected")
                self.voice = await self.vc.connect()
                self.is_connected = True
                await self.play_greeting()

            with yt_dlp.YoutubeDL(self.YDL_OPTIONS) as ydl:
                info_dict = ydl.extract_info(song, download=False)
                url = info_dict['url']

            audio_source = discord.FFmpegPCMAudio(url, executable=self.FFMPEG_EXECUTABLE, **self.FFMPEG_OPTIONS)

            self.voice.play(audio_source)
            self.music_queue.pop(0)
            while self.is_connected:
                while self.voice.is_playing():
                    await asyncio.sleep(0.1)

                if self.is_paused and not self.voice.is_playing():
                    while self.is_paused:
                        await asyncio.sleep(0.1)

                elif len(self.music_queue) == 0 and not self.is_paused and not self.voice.is_playing():
                    self.is_connected = False
                    self.is_playing = False
                    print("ENDING")
                    await self.voice.disconnect(force=True)
                elif len(self.music_queue) > 0 and not self.is_paused and not self.voice.is_playing():
                    song = str(self.music_queue[0])

                    with yt_dlp.YoutubeDL(self.YDL_OPTIONS) as ydl:
                        info_dict = ydl.extract_info(song, download=False)
                        url = info_dict['url']

                    audio_source = discord.FFmpegPCMAudio(url, executable=self.FFMPEG_EXECUTABLE, **self.FFMPEG_OPTIONS)

                    self.voice.play(audio_source)
                    self.music_queue.pop(0)

    # @commands.command(name="play", aliases=["p", "playing"], help="Plays a selected song from youtube")
    async def play(self, query, interaction):

        self.vc = interaction.author.voice.channel

        if self.vc is None:
            # you need to be connected so that the bot knows where to go
            return "Connect to a voice channel!"

        elif self.is_paused:
            self.vc.resume()

        elif self.is_playing:
            self.music_queue.append(query)
            print(self.music_queue)
        else:
            self.music_queue.append(query)
            print(self.music_queue)
            await self.play_music()

    # @commands.command(name="pause", help="Pauses the current song being played")
    async def pause(self):
        if not self.is_paused:
            self.is_paused = True
            self.voice.pause()
            print(self.is_paused)
            return "music paused"
        elif self.is_paused:
            self.is_paused = False
            self.voice.resume()
            return "music resumed"

    # @commands.command(name="resume", aliases=["r"], help="Resumes playing with the discord bot")
    async def resume(self):
        if self.is_paused:
            self.is_paused = False
            self.voice.resume()

    # @commands.command(name="skip", aliases=["s"], help="Skips the current song being played")
    async def skip(self):
        if self.vc != None and self.vc:
            self.vc.stop()
            # try to play next in the queue if it exists
            await self.play_music()

    # @commands.command(name="queue", aliases=["q"], help="Displays the current songs in queue")
    async def queue(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            # display a max of 5 songs in the current queue
            if (i > 4): break
            retval += self.music_queue[i][0]['title'] + "\n"

        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("No music in queue")

    # @commands.command(name="clear", aliases=["c", "bin"], help="Stops the music and clears the queue")
    async def clear_queue(self):
        self.music_queue = []

    # @commands.command(name="leave", aliases=["disconnect", "l", "d"], help="Kick the bot from VC")
    async def stop(self):
        self.is_playing = False
        self.is_paused = False
        self.is_connected = False
        await self.clear_queue()
        await self.voice.disconnect()

    async def play_greeting(self):
        self.voice.play(discord.FFmpegPCMAudio("StartUpGreeting.wav", executable=self.FFMPEG_EXECUTABLE))
        while self.voice.is_playing():
            await asyncio.sleep(0.1)
