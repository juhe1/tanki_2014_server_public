from client.layouts.battle_list import battle_list_codecs
from client.layouts.battle import battle_codecs
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class StatisticsTeamModelCommands:
    def __init__(self, space, game_object):
        self.space = space
        self.game_object = game_object
        self.CHANGE_TEAM_SCORE_COMMAND_ID = 300080013
        self.CHANGE_USER_STAT_COMMAND_ID = 300080014
        self.REFRESH_USERS_STAT_COMMAND_ID = 300080015
        self.SWAP_TEAM_COMMAND_ID = 300080016
        self.USER_CONNECTED_COMMAND_ID = 300080017
        self.USER_DISCONNECTED_COMMAND_ID = 300080018

    def change_team_score(self, team, score):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.CHANGE_TEAM_SCORE_COMMAND_ID, buffer)
        battle_list_codecs.TeamCodec.encode(team, buffer)
        basic_codecs.IntCodec.encode(score, buffer)
        self.space.send_command(self.game_object.id, buffer, "CHANGE_TEAM_SCORE")

    def change_user_stat(self, user_info, team):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.CHANGE_USER_STAT_COMMAND_ID, buffer)
        battle_codecs.UserStatCodec.encode(user_info, buffer)
        battle_list_codecs.TeamCodec.encode(team, buffer)
        self.space.send_command(self.game_object.id, buffer, "CHANGE_USER_STAT")

    def refresh_user_stat(self, user_infos, team):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.REFRESH_USERS_STAT_COMMAND_ID, buffer)
        basic_codecs.VectorLevel1Codec.encode(user_infos, battle_codecs.UserStatCodec, buffer)
        battle_list_codecs.TeamCodec.encode(team, buffer)
        self.space.send_command(self.game_object.id, buffer, "REFRESH_USERS_STAT")

    def swap_team(self, red_user_infos, blue_user_infos):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.SWAP_TEAM_COMMAND_ID, buffer)
        basic_codecs.VectorLevel1Codec.encode(red_user_infos, battle_codecs.UserStatCodec, buffer)
        basic_codecs.VectorLevel1Codec.encode(blue_user_infos, battle_codecs.UserStatCodec, buffer)
        self.space.send_command(self.game_object.id, buffer, "SWAP_TEAM")

    def user_connect(self, user_id, user_infos, team):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.USER_CONNECTED_COMMAND_ID, buffer)
        basic_codecs.LongCodec.encode(user_id, buffer)
        basic_codecs.VectorLevel1Codec.encode(user_infos, battle_codecs.UserInfoCodec, buffer)
        battle_list_codecs.TeamCodec.encode(team, buffer)
        self.space.send_command(self.game_object.id, buffer, "USER_CONNECTED")

    def user_disconnect(self, user_id):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.USER_DISCONNECTED_COMMAND_ID, buffer)
        basic_codecs.LongCodec.encode(user_id, buffer)
        self.space.send_command(self.game_object.id, buffer, "USER_CONNECTED")
