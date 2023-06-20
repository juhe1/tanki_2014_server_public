from client.layouts.battle_list import battle_list_codecs
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class TeamBattleItemModelCommands:
    def __init__(self, space, game_object):
        self.space = space
        self.game_object = game_object
        self.RELEASE_SLOT_COMMAND_ID = 300090034
        self.RESERVE_SLOT_COMMAND_ID = 300090035
        self.SWAP_TEAMS_COMMAND_ID = 300090036

    def release_slot(self, user_id):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.RELEASE_SLOT_COMMAND_ID, buffer)
        basic_codecs.LongCodec.encode(user_id, buffer)
        self.space.send_command(self.game_object.id, buffer, "RELEASE_SLOT")

    def reserve_slot(self, user_id, team):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.RESERVE_SLOT_COMMAND_ID, buffer)
        basic_codecs.LongCodec.encode(user_id, buffer)
        battle_list_codecs.TeamCodec.encode(team, buffer)
        self.space.send_command(self.game_object.id, buffer, "RESERVE_SLOT")

    def swap_teams(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.SWAP_TEAMS_COMMAND_ID, buffer)
        self.space.send_command(self.game_object.id, buffer, "SWAP_TEAMS")
