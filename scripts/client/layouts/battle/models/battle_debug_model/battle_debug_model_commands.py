from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class BattleDebugModelCommands:
    def __init__(self, space, game_object):
        self.space = space
        self.game_object = game_object
        self.ADD_MARKER_COMMAND_ID = 300100000

    def add_marker(self, size, color, position):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.ADD_MARKER_COMMAND_ID, buffer)
        basic_codecs.FloatCodec.encode(size, buffer)
        basic_codecs.IntCodec.encode(color, buffer)
        basic_codecs.Vector3DCodec.encode(position, buffer)
        self.space.send_command(self.game_object.id, buffer, "ADD_MARKER")
