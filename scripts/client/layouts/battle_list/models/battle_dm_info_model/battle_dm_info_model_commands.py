from client.layouts.battle_list import battle_list_codecs
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class BattleDmInfoModelCommands:
    def __init__(self, space, game_object):
        self.space = space
        self.game_object = game_object
        self.ADD_USER_COMMAND_ID = 300090008
        self.MOUNTED_ITEM_LOCKED_COMMAND_ID = 300090009
        self.UPDATE_USER_KILLS_COMMAND_ID = 300090010

    def add_user(self, user_info, team):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.ADD_USER_COMMAND_ID, buffer)
        battle_list_codecs.BattleInfoUserCodec.encode(user_info, buffer)
        self.space.send_command(self.game_object.id, buffer, "ADD_USER")

    def update_user_kills(self, user_info):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.UPDATE_USER_KILLS_COMMAND_ID, buffer)
        basic_codecs.LongCodec.encode(user_info.user_id, buffer)
        basic_codecs.IntCodec.encode(user_info.kills, buffer)
        self.space.send_command(self.game_object.id, buffer, "UPDATE_USER_KILLS")
