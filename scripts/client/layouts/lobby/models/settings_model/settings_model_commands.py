from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class SettingsModelCommands:
    def __init__(self, space, game_object):
        self.space = space
        self.game_object = game_object
        self.OPEN_SETTINGS_COMMAND_ID = 300050039

    def open_settings(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.OPEN_SETTINGS_COMMAND_ID, buffer)

        is_confirm_email = False # TODO: get this property from database
        is_news_send = False # TODO: get this property from database

        basic_codecs.BooleanCodec.encode(is_confirm_email, buffer)
        basic_codecs.BooleanCodec.encode(is_news_send, buffer)

        self.space.send_command(self.game_object.id, buffer, "OPEN_SETTINGS")
