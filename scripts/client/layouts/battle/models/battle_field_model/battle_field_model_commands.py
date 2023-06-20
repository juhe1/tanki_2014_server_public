from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class BattleFieldModelCommands:
    def __init__(self, space, game_object):
        self.space = space
        self.game_object = game_object
        self.BATTLE_FINISH_COMMAND_ID = 300100015
        self.BATTLE_RESTART_COMMAND_ID = 300100016

    def battle_finish(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.BATTLE_FINISH_COMMAND_ID, buffer)
        self.space.send_command(self.game_object.id, buffer, "BATTLE_FINISH")

    def battle_restart(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.BATTLE_RESTART_COMMAND_ID, buffer)
        self.space.send_command(self.game_object.id, buffer, "BATTLE_RESTART")
