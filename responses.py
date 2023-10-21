import random
from discord.ui import Button, View
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
    elif "radio" == p_message:
        print("Running radio")
        file_path = "radio.txt"
        buttons = read_info_text_from_file(file_path)

        for button in buttons:
            button.set_cog(music_bot)
            button.set_interaction(interaction)

        view = View()

        for button in buttons:
            view.add_item(button.button)

        await interaction.channel.send("Pick a radio:", view=view)

        for button in buttons:
            button.button.callback = button.button_callback

    elif "skip" == p_message:
        print("trying to skip")
        return await music_bot.skip()


    elif "pause" == p_message:
        print("Trying to pause")
        return await music_bot.pause()

    elif 'p test' == p_message:
        await music_bot.play("https://www.youtube.com/watch?v=zAnQg7uFQCI", interaction)

    elif "p " in p_message or "play" in p_message:
        url = p_message.split(" ")[1]
        return_string = await music_bot.play(url, interaction)
        return return_string

    elif "disconnect" == p_message or "stop" == p_message:
        print("Stop")
        result = music_bot.is_connected
        print(result)
        print(p_message)
        if result:
            await music_bot.stop()
            return "Disconnecting JiggleBack"
        else:
            return "Uhhhh did you mean that?"

    elif "random sound" in p_message:
        await music_bot.play_random_Sound(interaction, bot.directory, bot.ffmpeg_executable, bot.PLAY_SOUND_RANDOM_MAX)

    else:
        error_message: Embed = discord.Embed(
            description="Command not found. Type /help for a list of all available commands",
            color=0xFF5733)
        await interaction.channel.send(embed=error_message)


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
