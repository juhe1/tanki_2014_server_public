from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class BattleSelectModelCommands:
    def __init__(self, space, game_object):
        self.space = space
        self.game_object = game_object
        self.BATTLE_ITEMS_PACKET_JOIN_SUCCESS_ID = 300090026

    def battle_items_packet_join_success_id(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.BATTLE_ITEMS_PACKET_JOIN_SUCCESS_ID, buffer)
        self.space.send_command(self.game_object.id, buffer, "BATTLE_ITEMS_PACKET_JOIN_SUCCESS")
