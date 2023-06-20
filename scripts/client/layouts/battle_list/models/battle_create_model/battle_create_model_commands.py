from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class BattleCreateModelCommands:
    def __init__(self, space, game_object):
        self.space = space
        self.game_object = game_object
        self.SET_FILTTERED_BATTLE_NAME_COMMAND_ID = 300090006

    def set_filtered_battle_name(self, filtered_name):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.SET_FILTTERED_BATTLE_NAME_COMMAND_ID, buffer)
        basic_codecs.StringCodec.encode(filtered_name, buffer)
        self.space.send_command(self.game_object.id, buffer, "SET_FILTTERED_BATTLE_NAME")
