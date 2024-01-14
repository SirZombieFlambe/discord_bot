import audio_cog


class ServersSettings:
    def __init__(self, guild_id):
        self.guild_id = guild_id
        self.audio_cog = audio_cog.AudioCog(guild_id)
        self.annoyable_voice = False
        self.annoyable_text = False
        self.music_connect_start_sound = False
        self.setting_sudoer_list = []
        self.server_radios = {}


