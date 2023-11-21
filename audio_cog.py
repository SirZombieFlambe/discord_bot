import asyncio
import os
import random

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


async def disappointed_responses(amount_o_times):
    file = open('disappointed_phrases.txt')

    # read the content of the file opened
    disappointed_phrases = file.readlines()
    file.close()
    range_boi = len(disappointed_phrases) - 1
    print(range_boi)
    return disappointed_phrases[random.randint(0, range_boi)].format(amount_o_times)


async def pick_random_sound(directory):
    files = os.listdir(directory)
    files = [file for file in files if os.path.isfile(os.path.join(directory, file))]
    print(files)
    if files:
        track = str(random.choice(files))
        return directory + track


class audio_cog():

    def __init__(self):

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
        self.is_skipped = False

    def get_vc(self):
        return self.vc

    async def play_sound(self, url):
        audio_source = discord.FFmpegPCMAudio(url, executable=self.FFMPEG_EXECUTABLE, **self.FFMPEG_OPTIONS)

        self.voice.play(audio_source)

        self.music_queue.pop(0)
        while self.is_connected:

            while self.voice.is_playing() and not self.is_skipped:
                await asyncio.sleep(0.1)

            if self.is_paused and not self.voice.is_playing() and not self.is_skipped:
                while self.is_paused:
                    await asyncio.sleep(0.1)
                    print(self.is_skipped)

            elif len(self.music_queue) == 0 and not self.is_paused and not self.voice.is_playing():
                self.is_connected = False
                self.is_playing = False
                print("ENDING")
                await self.voice.disconnect(force=True)
            elif (len(self.music_queue) > 0 and not self.is_paused and not self.voice.is_playing()) or self.is_skipped:
                if self.is_skipped:
                    self.is_skipped = False
                    print("BREH BREH")


                song = str(self.music_queue[0])

                audio_source = discord.FFmpegPCMAudio((await self.find_url(song))[0], executable=self.FFMPEG_EXECUTABLE,
                                                      **self.FFMPEG_OPTIONS)

                self.voice.play(audio_source)
                self.music_queue.pop(0)

    async def find_url(self, query):
        with yt_dlp.YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info_dict = ydl.extract_info(query, download=False)
                return [info_dict['url'], True]
            except Exception:
                print(Exception)
                return ["", False]


    async def play_music(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            if not self.is_connected:
                self.voice = await self.vc.connect()
                self.is_connected = True
                #await self.play_greeting()

            song = str(self.music_queue[0])
            results = await self.find_url(song)
            success = results[1]
            await self.play_sound(results[0])
            if success is True:
                return ["STUFF Blah", success]
            else:
                print("AKLJSHDDHKJASHJK")
                return [f"I'm sorry, I cant find {song}. Are you sure you typed that right?", success]


        else:
            self.is_playing = False
            self.is_connected = False
            await self.voice.disconnect(force=True)

    # @commands.command(name="play", aliases=["p", "playing"], help="Plays a selected song from youtube")
    async def play(self, query, interaction):

        self.vc = interaction.author.voice.channel

        if self.vc is None:
            # you need to be connected so that the bot knows where to go
            return ["Connect to a voice channel!", False]

        elif self.is_paused:
            self.vc.resume()
            self.music_queue.append(query)

        elif self.is_playing:
            self.music_queue.append(query)
            print(self.music_queue)
        else:
            self.music_queue.append(query)
            print(self.music_queue)
            return await self.play_music()

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
        print("SKIPPING")
        if self.is_playing:
            self.is_skipped = True
            self.voice.pause()
            print(self.music_queue)
            return "Skipped"


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

    async def play_random_Sound(self, interaction, directory, ffmpeg_executable, PLAY_SOUND_RANDOM_MAX):
        user_message = str(interaction.content)
        username = str(interaction.author)

        self.vc = interaction.author.voice.channel

        if self.vc is None:
            # you need to be connected so that the bot knows where to go
            return "Connect to a voice channel!"

        if user_message == "random sound":

            self.voice = await self.vc.connect()
            self.voice.play(
                discord.FFmpegPCMAudio(await pick_random_sound(directory), executable=ffmpeg_executable))
            while self.voice.is_playing():
                await asyncio.sleep(0.1)

            if not self.voice.is_playing():
                await self.voice.disconnect()

        print(user_message)
        amount_o_times = user_message.rsplit('x')[1]

        if amount_o_times.isdigit():

            if int(amount_o_times) < int(PLAY_SOUND_RANDOM_MAX):

                await interaction.channel.send(f'Playing sounds for {amount_o_times} times')

                self.voice = await self.vc.connect()

                for x in range(int(amount_o_times)):

                    self.voice.play(
                        discord.FFmpegPCMAudio(await pick_random_sound(directory), executable=ffmpeg_executable))
                    while self.voice.is_playing():
                        await asyncio.sleep(0.1)

                await self.voice.disconnect(force=True)

            elif (int(amount_o_times) >= int(PLAY_SOUND_RANDOM_MAX)) and (username == "yifendes"):

                for x in range(int(amount_o_times)):
                    await interaction.author.send(await disappointed_responses(amount_o_times))

            else:

                await interaction.channel.send(await disappointed_responses(amount_o_times))
