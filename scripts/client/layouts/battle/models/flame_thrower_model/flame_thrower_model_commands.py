from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class FlameThrowerModelCommands:
    def __init__(self, space, game_object):
        self.space = space
        self.game_object = game_object
        self.FIRE_COMMAND_ID = 300100041
        self.STOP_COMMAND_ID = 300100042

    def start_fire(self, shooter_id):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.FIRE_COMMAND_ID, buffer)
        basic_codecs.LongCodec.encode(shooter_id, buffer)
        self.space.send_command(self.game_object.id, buffer, "FIRE")

    def stop_fire(self, shooter_id):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.STOP_COMMAND_ID, buffer)
        basic_codecs.LongCodec.encode(shooter_id, buffer)
        self.space.send_command(self.game_object.id, buffer, "STOP_FIRE")
