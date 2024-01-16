import audio_cog


class ServersSettings:
    def __init__(self, guild):
        self.guild_id = guild.id
        self.audio_cog = audio_cog.AudioCog(guild.id)
        self.server_annoyable_voice = False
        self.server_annoyable_text = False
        self.music_connect_start_sound = False
        self.setting_sudoer_list = [str(guild.owner.name)]
        self.annoyable = []
        self.server_radios = {}
        self.guild_info = guild


    def print_settings(self):
        print(f'Guild ID: {self.guild_id}')
        print(f'Audio Cog: {self.audio_cog}')
        print(f'Joins audio when these people join: {self.server_annoyable_voice}')
        print(f'Sends a message to these people when they join: {self.server_annoyable_text}')
        print(f'Play when music starts: {self.music_connect_start_sound}')
        print(f"Server's Sudoers: {self.setting_sudoer_list}")
        print(f"Server's radios: {self.server_radios}")


    def get_setting(self):
        if self.guild_id is None:
            return "There are no guilds yet"
        else:
            return (f'Guild ID, {self.guild_id}\nGuild Name, {self.guild_info}\nAudio cog, {self.audio_cog}'
                    f'\nServer Annoy-able voice, {self.server_annoyable_voice}'
                    f'\nServer Annoy-able text, {self.server_annoyable_text}'
                    f'\nAnnoy-able users, {self.annoyable}'
                    f'\nConnect start sound, {self.music_connect_start_sound}'
                    f'\nServer sudoer\'s list, {self.setting_sudoer_list}'
                    f'\nServer radios, {self.server_radios}')

    async def addSudoer(self):
        print(",kld bhjsnfz")

class Annoyable:
    def __init__(self, user):
        self.annoyable_user = user
        self.annoyable_voice = False
        self.annoyable_text = False