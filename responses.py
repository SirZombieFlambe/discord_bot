import random
from discord.ui import Button, View
import discord
from discord import Embed

import bot
import colors






async def get_response(interaction):

    audio_bot = bot.audio_bot

    try:
        p_message = str(interaction.content)
        print(p_message)
        if p_message == 'hello':
            return_message: Embed = discord.Embed(
                description="Howdy",
                color=colors.yellow
            )
            return return_message

        elif "check12" in p_message:
            return_message: Embed = discord.Embed(
                description=audio_bot.is_playing,
                color=colors.yellow
            )
            return return_message


        elif "jiffy" in p_message:
            p_message = p_message.rsplit("jiffy")[1]
            p_message = p_message.split()
            pp_message = ""

            for word in list(p_message):
                temp_list = list(word)
                temp_list[0] = "j"

                pp_message = pp_message + " " + word[0:].replace(word[0], "j", 1)

            return_message: Embed = discord.Embed(
                description=pp_message,
                color=colors.mediumpurple
            )
            return return_message



        elif p_message == 'roll':

            return_message: Embed = discord.Embed(
                description= "Rrrrrollling: {0}".format(str(random.randint(1, 6))),
                color=colors.mediumturquoise
            )
            return return_message

        elif p_message == '/help':
            all_commands = """ ```
All commands:
/help - displays all the available commands
/phelp - displays all the available Music commands

<Chat Commands>
!hello - says hi to the user
!jiffy - [Whatever words turned to "jords" that make up "jentences"]
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
            return_message: Embed = discord.Embed(
                description=all_commands,
                color=colors.green
            )
            return return_message

        elif p_message == '/phelp':
            music_commands = """ ```
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
            return_message: Embed = discord.Embed(
                description=music_commands,
                color=colors.darkgreen
            )
            return return_message

        elif p_message == 'help':
            general_commands = """ ```
General commands:
/help - displays all the available commands
!random sound [xAMOUNT OF TIMES WANTED TO PLAY... Be nice]
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
            return_message: Embed = discord.Embed(
                description=general_commands,
                color=colors.lawngreen
            )
            return return_message

        elif "radio" == p_message:
            print("Running radio")
            file_path = "radio.txt"
            buttons = read_info_text_from_file(file_path)

            for button in buttons:
                button.set_cog(audio_bot)
                button.set_interaction(interaction)

            view = View()

            for button in buttons:
                view.add_item(button.button)

            await interaction.channel.send("Pick a radio:", view=view)

            for button in buttons:
                button.button.callback = button.button_callback

        elif "skip" == p_message:
            print("trying to skip")
            result = await audio_bot.skip()
            return_message: Embed = discord.Embed(
                description=result,
                color=colors.ceruleanblue
            )
            return return_message

        elif "pause" == p_message:
            print("Trying to pause")
            result = await audio_bot.pause()
            return_message: Embed = discord.Embed(
                description=result,
                color=colors.red
            )
            return return_message


        elif 'p test' == p_message:
            results = await audio_bot.play("https://www.youtube.com/watch?v=zAnQg7uFQCI", interaction)
            description = "Audio Test"
            color = colors.burlywood
            if results[1] is not True:
                color = colors.maroon
                description = results[0]

            return_message: Embed = discord.Embed(
                description=description,
                color=color
            )
            return return_message


        elif "p " in p_message or "play" in p_message:
            url = p_message.split(" ")[1]
            results = await audio_bot.play(url, interaction)
            if results[1] is not True:
                color = colors.maroon
                return_message: Embed = discord.Embed(
                    description=results[0],
                    color=color)
                return return_message

        elif "disconnect" == p_message or "stop" == p_message:
            print("Stop")
            result = audio_bot.is_connected
            print(result)
            print(p_message)
            if result:
                await audio_bot.stop()
                return_message: Embed = discord.Embed(
                    description="Disconnecting JiggleBack",
                    color=colors.green)
                return return_message
            else:
                return_message: Embed = discord.Embed(
                    description="Uhhhh did you mean that?",
                    color=colors.firebrick)
                return return_message

        elif "random sound" in p_message:
            await audio_bot.play_random_Sound(interaction, bot.directory, bot.ffmpeg_executable, bot.PLAY_SOUND_RANDOM_MAX)


        else:
            error_message: Embed = discord.Embed(
                description="Command not found. Type /help for a list of all available commands",
                color=colors.outrageousorange)
            return error_message

    except Exception as e:

        print(f'{e} soooo error')


def read_info_text_from_file(file_path):
    embeded = []
    with open(file_path, 'r', encoding='utf-8') as file:
        i = 0
        for line in file:
            current_line = line
            title = current_line.split('title="')[1].split('" description=')[0]
            description = current_line.split('description="')[1].split('" url=')[0]
            url = current_line.split(" url='")[1].split("' color=")[0]
            color = current_line.split("color=")[1]
            embeded.append(EmbededMessages(title, description, url, color))
            i = i + 1

    return embeded


class EmbededMessages:

    def __init__(self, title, description, url, color):
        self.title = title
        self.description = description
        self.url = url
        self.color = int(color.split("\n")[0], 16)
        self.audio_cog = None
        self.interaction = None
        self.button = Button(label=self.description, style=discord.ButtonStyle.blurple, emoji="▶️")

    async def button_callback(self, button_interaction):
        embed = discord.Embed(title=self.title, description=self.description, url=self.url,
                              color=self.color)
        await button_interaction.response.send_message(embed=embed)
        await self.audio_cog.play(self.url, self.interaction)

    def set_cog(self, audio_cog):
        self.audio_cog = audio_cog

    def set_interaction(self, interaction):
        self.interaction = interaction
