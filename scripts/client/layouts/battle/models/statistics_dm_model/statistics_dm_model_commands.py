from client.layouts.battle import battle_codecs
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class StatisticsDmModelCommands:
    def __init__(self, space, game_object):
        self.space = space
        self.game_object = game_object
        self.USER_CONNECTED_COMMAND_ID = 300080004
        self.USER_DISCONNECTED_COMMAND_ID = 300080005
        self.CHANGE_USER_STAT_COMMAND_ID = 300080002
        self.REFRESH_USERS_STAT_COMMAND_ID = 300080002

    def user_connected(self, user_id, user_info_list):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.USER_CONNECTED_COMMAND_ID, buffer)
        basic_codecs.LongCodec.encode(user_id, buffer)
        basic_codecs.VectorLevel1Codec.encode(user_info_list, battle_codecs.UserInfoCodec, buffer)
        self.space.send_command(self.game_object.id, buffer, "USER_CONNECTED")

    def user_disconnected(self, user_id):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.USER_DISCONNECTED_COMMAND_ID, buffer)
        basic_codecs.LongCodec.encode(user_id, buffer)
        self.space.send_command(self.game_object.id, buffer, "USER_DISCONNECTED")

    def change_user_stat(self, user_info):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.CHANGE_USER_STAT_COMMAND_ID, buffer)
        battle_codecs.UserStatCodec.encode(user_info, buffer)
        self.space.send_command(self.game_object.id, buffer, "CHANGE_USER_STAT")

    def refresh_user_stat(self, user_infos):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.REFRESH_USERS_STAT_COMMAND_ID, buffer)
        basic_codecs.VectorLevel1Codec.encode(user_infos, battle_codecs.UserStatCodec, buffer)
        self.space.send_command(self.game_object.id, buffer, "REFRESH_USERS_STAT")
