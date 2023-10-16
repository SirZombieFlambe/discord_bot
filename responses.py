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

        button1 = Button(label=buttons[0].description, style=discord.ButtonStyle.blurple, emoji="▶️")
        button2 = Button(label=buttons[1].description, style=discord.ButtonStyle.blurple, emoji="▶️")
        button3 = Button(label=buttons[2].description, style=discord.ButtonStyle.blurple, emoji="▶️")

        async def button_callback1(button_interaction):
            embed = discord.Embed(title=buttons[0].title, description=buttons[0].description, url=buttons[0].url,
                                  color=buttons[0].color)
            await button_interaction.response.send_message(embed=embed)
            await music_bot.play(buttons[0].url, interaction)

        async def button_callback2(button_interaction):
            embed = discord.Embed(title=buttons[1].title, description=buttons[1].description, url=buttons[1].url,
                                  color=buttons[1].color)
            await button_interaction.response.send_message(embed=embed)
            await music_bot.play(buttons[1].url, interaction)

        async def button_callback3(button_interaction):
            embed = discord.Embed(title=buttons[2].title, description=buttons[2].description, url=buttons[2].url,
                                  color=buttons[2].color)
            await button_interaction.response.send_message(embed=embed)
            await music_bot.play(buttons[2].url, interaction)

        view = View()
        view.add_item(button1)
        view.add_item(button2)
        view.add_item(button3)
        await interaction.channel.send("Pick a radio:", view=view)
        button1.callback = button_callback1
        button2.callback = button_callback2
        button3.callback = button_callback3

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
