from client.layouts.battle_list import battle_list_codecs
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class TeamBattleInfoModelCommands:
    def __init__(self, space, game_object):
        self.space = space
        self.game_object = game_object
        self.ADD_USER_COMMAND_ID = 300090029
        self.MOUNTED_ITEM_LOCKED_COMMAND_ID = 300090030
        self.SWAP_TEAMS_COMMAND_ID = 300090031
        self.UPDATE_TEAM_SCORE_COMMAND_ID = 300090032
        self.UPDATE_USER_SCORE_COMMAND_ID = 300090033

    def add_user(self, user_info, team):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.ADD_USER_COMMAND_ID, buffer)
        battle_list_codecs.BattleInfoUserCodec.encode(user_info, buffer)
        battle_list_codecs.TeamCodec.encode(team, buffer)
        self.space.send_command(self.game_object.id, buffer, "ADD_USER")

    def swap_teams(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.SWAP_TEAMS_COMMAND_ID, buffer)
        self.space.send_command(self.game_object.id, buffer, "SWAP_TEAMS")

    def update_team_score(self, score, team):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.UPDATE_TEAM_SCORE_COMMAND_ID, buffer)
        battle_list_codecs.TeamCodec.encode(team, buffer)
        basic_codecs.IntCodec.encode(score, buffer)
        self.space.send_command(self.game_object.id, buffer, "UPDATE_TEAM_SCORE")

    def update_user_score(self, user_id, score):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.UPDATE_USER_SCORE_COMMAND_ID, buffer)
        basic_codecs.LongCodec.encode(user_id, buffer)
        basic_codecs.IntCodec.encode(score, buffer)
        self.space.send_command(self.game_object.id, buffer, "UPDATE_USER_SCORE")

