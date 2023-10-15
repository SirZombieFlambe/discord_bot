import asyncio
import os
import random

import discord
from discord import Embed

import bot


async def get_response(music_bot, interaction):
    p_message = str(interaction.content)

    if p_message == 'hello':
        return 'UwU Master'


    elif p_message == 'roll':
        return "Rrrrrollling :{0}".format(str(random.randint(1, 6)))

    elif p_message == '/help':
        return """ ```
        All commands:
        /help - displays all the available commands
        /phelp - displays all the available Music commands
        <Chat Commands>
        !Hello - says hi to the user
        !roll - Rolls a 1d6
        <Random Commands>
        !random sound [xAMOUNT OF TIMES WANTED TO PLAY... Be nice]
        <Music Bot Commands>
        !p <keywords> - finds the song on youtube and plays it in your current channel. Will resume playing the current 
            song if it was paused
        !q - displays the current music queue
        !skip - skips the current song being played
        !clear - Stops the music and clears the queue
        !leave - Disconnected the bot from the voice channel
        !pause - pauses the current song being played or resumes if already paused
        !resume - resumes playing the current song
        

                       ```
                       """

    elif p_message == '/phelp':
        return """ ```
            Music commands:
            !help - displays all Music Commands
            !p <keywords> - finds the song on youtube and plays it in your current channel. Will resume playing the current 
                song if it was paused
            !q - displays the current music queue
            !skip - skips the current song being played
            !clear - Stops the music and clears the queue
            !leave - Disconnected the bot from the voice channel
            !pause - pauses the current song being played or resumes if already paused
            !resume - resumes playing the current song

                           ```
                           """

    elif p_message == 'help':
        return """ ```
General commands:
/help - displays all the available commands
!random sound [xAMOUNT OF TIMES WANTED TO PLAY... Be nice]
!p <keywords> - finds the song on youtube and plays it in your current channel. Will resume playing the current song if it was paused
!q - displays the current music queue
!skip - skips the current song being played
!clear - Stops the music and clears the queue
!leave - Disconnected the bot from the voice channel
!pause - pauses the current song being played or resumes if already paused
!resume - resumes playing the current song
        
               ```
               """

    elif 'p test' in p_message:
        await music_bot.play("https://www.youtube.com/watch?v=zAnQg7uFQCI", interaction)

    elif "p " in p_message or "play" in p_message:
        url = p_message.split(" ")[1]
        return_string = await music_bot.play(url, interaction)
        return return_string

    elif "pause" == p_message:
        print("Trying to pause")
        return await music_bot.pause()

    elif "disconnect" or "stop" == p_message:
        print("Stop")
        result = music_bot.is_connected
        print(result)
        if result:
            await music_bot.stop()
        else:
            await voice.disconnect()
        return "Disconnecting JiggleBack"


    else:
        error_message: Embed = discord.Embed(
            description="Command not found. Type /help for a list of all available commands",
            color=0xFF5733)
        await interaction.channel.send(embed=error_message)


async def pick_random_sound(directory):
    files = os.listdir(directory)
    files = [file for file in files if os.path.isfile(os.path.join(directory, file))]
    print(files)
    if files:
        track = str(random.choice(files))
        return directory + track


async def play_random_Sound(interaction, directory, ffmpeg_executable, PLAY_SOUND_RANDOM_MAX):
    user_message = str(interaction.content)
    username = str(interaction.author)

    voice_channel = interaction.author.voice.channel

    if user_message == "random sound":
        global voice
        voice = await voice_channel.connect()
        voice.play(discord.FFmpegPCMAudio(await pick_random_sound(directory), executable=ffmpeg_executable))
        while voice.is_playing():
            await asyncio.sleep(0.1)

        if not voice.is_playing():
            await voice.disconnect()

    print(user_message)
    amount_o_times = user_message.rsplit('x')[1]

    if amount_o_times.isdigit():

        if int(amount_o_times) < int(PLAY_SOUND_RANDOM_MAX):

            await interaction.channel.send(f'Playing sounds for {amount_o_times} times')

            voice = await voice_channel.connect()

            for x in range(int(amount_o_times)):

                voice.play(discord.FFmpegPCMAudio(await pick_random_sound(directory), executable=ffmpeg_executable))
                while voice.is_playing():
                    await asyncio.sleep(0.1)

            await voice.disconnect(force=True)

        elif (int(amount_o_times) >= int(PLAY_SOUND_RANDOM_MAX)) and (username == "yifendes"):

            for x in range(int(amount_o_times)):
                await interaction.author.send(await disappointed_responses(amount_o_times))

        else:

            await interaction.channel.send(await disappointed_responses(amount_o_times))


async def disappointed_responses(amount_o_times):
    file = open('disappointed_phrases.txt')

    # read the content of the file opened
    disappointed_phrases = file.readlines()
    range_boi = len(disappointed_phrases) - 1
    print(range_boi)
    return disappointed_phrases[random.randint(0, range_boi)].format(amount_o_times)


