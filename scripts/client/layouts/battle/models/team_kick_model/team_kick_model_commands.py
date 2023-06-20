from client.layouts.battle import battle_codecs
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class TeamKickModelCommands:
    def __init__(self, space, game_object):
        self.space = space
        self.game_object = game_object
        self.ALLOW_VOTING_COMMAND_ID = 300080020
        self.EXCLUDE_COMMAND_ID = 300080021
        self.FINISH_VOTING_COMMAND_ID = 300080022
        self.USER_CONNECTED_COMMAND_ID = 300080023
        self.USER_DISCONNECT_COMMAND_ID = 300080024
        self.UPDATE_VOTES_COMMAND_ID = 300080025

    def allow_voting(self, user_id, votes):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.ALLOW_VOTING_COMMAND_ID, buffer)
        basic_codecs.LongCodec.encode(user_id, buffer)
        basic_codecs.ShortCodec.encode(votes, buffer)
        self.space.send_command(self.game_object.id, buffer, "ALLOW_VOTING")

    def exclude(self, user_id):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.EXCLUDE_COMMAND_ID, buffer)
        basic_codecs.LongCodec.encode(user_id, buffer)
        self.space.send_command(self.game_object.id, buffer, "EXCLUDE")

    def finish_voting(self, user_id):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.FINISH_VOTING_COMMAND_ID, buffer)
        basic_codecs.LongCodec.encode(user_id, buffer)
        self.space.send_command(self.game_object.id, buffer, "FINISH_VOTING")

    def user_connected(self, user_team_kick_data):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.USER_CONNECTED_COMMAND_ID, buffer)
        battle_codecs.UserTeamKickDataCodec.encode(user_team_kick_data, buffer)
        self.space.send_command(self.game_object.id, buffer, "USER_CONNECTED")

    def user_disconnect(self, user_id):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.USER_DISCONNECT_COMMAND_ID, buffer)
        basic_codecs.LongCodec.encode(user_id, buffer)
        self.space.send_command(self.game_object.id, buffer, "USER_DISCONNECT")

    def update_votes(self, user_id, votes):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.UPDATE_VOTES_COMMAND_ID, buffer)
        basic_codecs.LongCodec.encode(user_id, buffer)
        basic_codecs.ShortCodec.encode(votes, buffer)
        self.space.send_command(self.game_object.id, buffer, "UPDATE_VOTES")


