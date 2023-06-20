from client.layouts.garage import garage_codecs
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer
from utils.log import console_out

class UpgradingItemsModelCommands:
    def __init__(self, space, game_object):
        self.space = space
        self.game_object = game_object

        self.INIT_COMMAND_ID = 300050053

    def init(self, upgraded_items, upgrading_items):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.INIT_COMMAND_ID, buffer)
        basic_codecs.VectorLevel1Codec.encode(upgraded_items, garage_codecs.GarageItemInfo, buffer)
        basic_codecs.VectorLevel1Codec.encode(upgrading_items, garage_codecs.GarageItemInfo, buffer)

        self.space.send_command(self.game_object.id, buffer, "INIT UPGRADING ITEMS")
