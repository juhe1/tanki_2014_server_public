from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class GarageModelCommands:
    def __init__(self, space, game_object):
        self.space = space
        self.game_object = game_object

        self.INIT_DEPOT_COMMAND_ID = 300040005
        self.INIT_MARKET_COMMAND_ID = 300040006
        self.INIT_MOUNTED_COMMAND_ID = 300040007
        self.SELECT_COMMAND_ID = 300040009

    def init_depot(self, items):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.INIT_DEPOT_COMMAND_ID, buffer)
        basic_codecs.VectorLevel1Codec.encode(items, basic_codecs.LongCodec, buffer)
        self.space.send_command(self.game_object.id, buffer, "INIT_DEPOT")

    def init_market(self, items):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.INIT_MARKET_COMMAND_ID, buffer)
        basic_codecs.VectorLevel1Codec.encode(items, basic_codecs.LongCodec, buffer)
        self.space.send_command(self.game_object.id, buffer, "INIT_MARKET")

    def init_mounted(self, items):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.INIT_MOUNTED_COMMAND_ID, buffer)
        basic_codecs.VectorLevel1Codec.encode(items, basic_codecs.LongCodec, buffer)
        self.space.send_command(self.game_object.id, buffer, "INIT_MOUNTED")

    def select(self, item_game_object_id):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.SELECT_COMMAND_ID, buffer)
        basic_codecs.LongCodec.encode(item_game_object_id, buffer)
        self.space.send_command(self.game_object.id, buffer, "SELECT_COMMAND")
