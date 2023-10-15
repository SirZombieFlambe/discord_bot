import asyncio
import os
import random

import discord

import responses
# from discord.ext import commands
from audio_cog import audio_cog


async def send_message(interaction, is_private, music_bot):
    # Function code here

    try:
        response = await responses.get_response(music_bot, interaction)
        await interaction.author.send(response) if is_private else await interaction.channel.send(response)

    except Exception as e:

        print(f'{e} soooo error')
async def send_is_connected_error(interaction):
    await interaction.channel.send("The bot is currently playing audio, please wait until audio finishes")


def run_discord_bot(TOKEN_1):
    intents = discord.Intents.default()
    intents.message_content = True
    client_1 = discord.Client(intents=intents)

    directory = "D:/Sound Board/discord/"
    ffmpeg_executable = "D:/RandomDownload/ffmpeg.exe"
    PLAY_SOUND_RANDOM_MAX = '16'


    audio_bot = audio_cog()

    @client_1.event
    async def on_ready():
        print(f'{client_1.user} is now running!')

    sudoers_file = "sudoers_list.txt"  # Replace with your file path
    with open(sudoers_file, 'r') as file:
        allowed_users = [line.strip() for line in file]

    @client_1.event
    async def on_voice_state_update(member, before, after):

        if member.name == client_1.user:
            return

        if not before.channel and after.channel and (member.name in allowed_users):
            userid = member.id
            user = await client_1.fetch_user(userid)

            await user.send(get_random_greeting())

            files = os.listdir(directory)
            files = [file for file in files if os.path.isfile(os.path.join(directory, file))]


            if files:

                track = str(random.choice(files))
                if not audio_bot.is_connected:

                    voice_channel = after.channel
                    voice = await voice_channel.connect()
                    audio_bot.is_connected = True

                else:
                    voice = audio_bot.voice

                voice.play(discord.FFmpegPCMAudio(directory + track, executable=ffmpeg_executable))


                while voice.is_playing():
                    await asyncio.sleep(0.1)

                if not voice.is_playing():
                    await voice.disconnect()
                    audio_bot.is_connected = False

            else:
                print("No audio files found in the directory.")

    @client_1.event
    async def on_message(interaction):

        if interaction.author == client_1.user:
            return
        username = str(interaction.author)
        user_message = str(interaction.content)
        channel = str(interaction.channel)

        # print({interaction.author.voice})

        print(f'{username} said: "{user_message}" ({channel})')
        if user_message.startswith('!'):

            interaction.content = (user_message.rsplit('!'))[1]
            print(user_message)
            if user_message[0] == '?':

                await send_message(interaction, True, audio_bot)
            elif "random sound" in user_message:
                if audio_bot.is_connected:
                    await send_is_connected_error(interaction)
                else:
                    await responses.play_random_Sound(interaction, directory, ffmpeg_executable, PLAY_SOUND_RANDOM_MAX)

            elif user_message == '!restart':

                await restart(interaction)

            else:

                await send_message(interaction, False, audio_bot)
        elif user_message.startswith('/'):
            print(user_message)
            await send_message(interaction, False, audio_bot)

    def get_random_greeting():
        greetings_file = "uwu_greetings.txt"  # Replace with your file path
        with open(greetings_file, "r", encoding="utf-8") as file2:
            greetings = file2.readlines()

        # Choose a random greeting
        random_greeting = random.choice(greetings)
        return random_greeting

    async def restart(interaction):

        print(interaction.author.name)
        current_file = open("sudoers_list.txt")
        allowed_sudo_user = current_file.readlines()
        for i in range(len(allowed_sudo_user)):
            allowed_sudo_user[i] = allowed_sudo_user[i].strip('\n')

        author = interaction.author.name

        if author in allowed_sudo_user:
            def check(message):
                return message.author == interaction.author and message.channel.type == discord.ChannelType.private

            try:

                await interaction.author.send("Enter the Password: ")
                password_message = await client_1.wait_for("message", timeout=30,
                                                           check=check)  # You can adjust the timeout as needed

                # Check if the password is correct
                if password_message.content == "thiccus diccus":
                    
                    await interaction.channel.send("Password is correct. Restarting...")
                    await audio_bot.clear_queue()
                    await client_1.close()
                else:
                    await interaction.author.send("Incorrect password. Restart aborted.")
            except asyncio.TimeoutError:
                await interaction.author.send("You didn't provide a password in time. Restart aborted.")
        else:
            await interaction.author.send(f"{author} not found in list of sudoers")

    client_1.run(TOKEN_1)
