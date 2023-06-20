from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class BattleDmItemModelCommands:
    def __init__(self, space, game_object):
        self.space = space
        self.game_object = game_object
        self.RELEASE_SLOT_COMMAND_ID = 300090011
        self.RESERVE_SLOT_COMMAND_ID = 300090012

    def release_slot(self, user_id):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.RELEASE_SLOT_COMMAND_ID, buffer)
        basic_codecs.LongCodec.encode(user_id, buffer)
        self.space.send_command(self.game_object.id, buffer, "RELEASE_SLOT")

    def reserve_slot(self, user_id, team):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.RESERVE_SLOT_COMMAND_ID, buffer)
        basic_codecs.LongCodec.encode(user_id, buffer)
        self.space.send_command(self.game_object.id, buffer, "RESERVE_SLOT")
