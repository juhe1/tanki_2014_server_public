from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class LoginModelCommands:
    def __init__(self, space, game_object):
        self.space = space
        self.game_object = game_object
        self.WRONG_PASSWORD_COMMAND_ID = 300020049

    def wrong_password(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.WRONG_PASSWORD_COMMAND_ID, buffer)
        self.space.send_command(self.game_object.id, buffer, "WRONG_PASSWORD")
