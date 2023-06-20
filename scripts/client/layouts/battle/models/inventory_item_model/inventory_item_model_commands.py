from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class InventoryItemModelCommands:
    def __init__(self, space, game_object):
        self.space = space
        self.game_object = game_object
        self.ACTIVATE_COMMAND_ID = 300100049

    def activate(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.ACTIVATE_COMMAND_ID, buffer)
        self.space.send_command(self.game_object.id, buffer, "ACTIVATE")
