import asyncio
import os
import random

import discord
import audio_cog
import responses as resp
# from discord.ext import commands
import audio_cog


async def send_message(interaction, message, is_private=False):
    # Function code here

    await interaction.author.send(embed=message) if is_private else await interaction.channel.send(embed=message)


async def send_is_connected_error(interaction):
    await interaction.channel.send("The bot is currently playing audio, please wait until audio finishes")


directory = 'D:/Sound Board/discord/'
cringe_directory = 'D:/CodingDev/Python/discordBot/cringe/'
ffmpeg_executable = "D:/CodingDev/Python/discordBot/FFMPEG/ffmpeg.exe"
PLAY_SOUND_RANDOM_MAX = '16'
audio_cogs = {}


def run_discord_bot(TOKEN_1):
    intents = discord.Intents.default()
    intents.message_content = True
    client_1 = discord.Client(intents=intents)
    sudoers_file = "sudoers_list.txt"  # Replace with your file path
    with open(sudoers_file, 'r') as file:
        allowed_users = [line.strip() for line in file]
    file.close()

    @client_1.event
    async def on_ready():
        print(f'{client_1.user} is now running!')

    @client_1.event
    async def on_voice_state_update(member, before, after):

        if member.id == client_1.user.id:  # Check if the member is the bot
            return

        if (after.channel is not None) and (str(member) in allowed_users):

            guild_id = member.guild.id
            userid = member.id

            audio_check(guild_id)

            user = await client_1.fetch_user(userid)
            await user.send(get_random_greeting())

            files = os.listdir(directory)
            files = [file for file in files if os.path.isfile(os.path.join(directory, file))]

            if files:

                track = str(random.choice(files))
                if not audio_cogs[guild_id].is_connected:

                    voice_channel = after.channel
                    voice = await voice_channel.connect()
                    audio_cogs[guild_id].is_connected = True

                else:
                    voice = audio_cogs[guild_id].voice

                voice.play(discord.FFmpegPCMAudio(directory + track, executable=ffmpeg_executable))

                while voice.is_playing():
                    await asyncio.sleep(0.1)

                if not voice.is_playing():
                    await voice.disconnect()
                    audio_cogs[guild_id].is_connected = False

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

                await send_message(interaction, await resp.get_response(interaction), is_private=True)

            elif user_message == '!restart':

                await restart(interaction)

            else:

                await send_message(interaction, await resp.get_response(interaction))

        elif user_message.startswith('/'):
            print(user_message)
            await send_message(interaction, await resp.get_response(interaction))

    def get_random_greeting():
        greetings_file = "uwu_greetings.txt"  # Replace with your file path
        with open(greetings_file, "r", encoding="utf-8") as file2:
            greetings = file2.readlines()
        file2.close()
        # Choose a random greeting
        random_greeting = random.choice(greetings)
        return random_greeting



    async def restart(interaction):

        print(interaction.author.name)
        current_file = open("sudoers_list.txt")
        allowed_sudo_user = current_file.readlines()
        current_file.close()
        for i in range(len(allowed_sudo_user)):
            allowed_sudo_user[i] = allowed_sudo_user[i].strip('\n')

        author = interaction.author.name

        if author in allowed_sudo_user:
            def check(message):
                return (
                        message.author == interaction.author
                        and isinstance(message.channel, discord.DMChannel)
                )

            try:
                #guild_id = interaction.author.guild.id
                await interaction.author.send("Enter the Password: ")
                password_message = await client_1.wait_for("message", timeout=30,
                                                           check=check)  # You can adjust the timeout as needed

                # Check if the password is correct
                if password_message.content == "BREH":

                    await interaction.channel.send("Password is correct. Restarting...")
                    for guild in audio_cogs:
                        await audio_cogs[guild].clear_queue()

                    await client_1.close()
                else:
                    await interaction.author.send("Incorrect password. Restart aborted.")
            except asyncio.TimeoutError:
                await interaction.author.send("You didn't provide a password in time. Restart aborted.")
        else:
            await interaction.author.send(f"{author} not found in list of sudoers")

    client_1.run(TOKEN_1)

def audio_check(guild_id):
    if guild_id not in audio_cogs:
        audio_cogs[guild_id] = audio_cog.AudioCog(guild_id)