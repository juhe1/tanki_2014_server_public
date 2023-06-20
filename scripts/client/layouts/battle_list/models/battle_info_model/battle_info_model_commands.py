from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class BattleInfoModelCommands:
    def __init__(self, space, game_object):
        self.space = space
        self.game_object = game_object

        self.REMOVE_USER_COMMAND_ID = 300090016
        self.FINISH_ROUND_COMMAND_ID = 300090017
        self.START_ROUND_COMMAND_ID = 300090018

    def remove_user(self, user_id):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.REMOVE_USER_COMMAND_ID, buffer)
        basic_codecs.LongCodec.encode(user_id, buffer)
        self.space.send_command(self.game_object.id, buffer, "REMOVE_USER")

    def finish_round(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.FINISH_ROUND_COMMAND_ID, buffer)
        self.space.send_command(self.game_object.id, buffer, "FINISH_ROUND")

    def start_round(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.START_ROUND_COMMAND_ID, buffer)
        self.space.send_command(self.game_object.id, buffer, "START_ROUND")
