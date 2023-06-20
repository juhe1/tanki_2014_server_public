from client.layouts.battle import battle_codecs
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class StatisticsModelCommands:
    def __init__(self, space, game_object):
        self.space = space
        self.game_object = game_object
        self.FUND_CHANGE_COMMAND_ID = 300080007
        self.ROUND_FINISH_COMMAND_ID = 300080010
        self.ROUND_START_COMMAND_ID = 300080011
        self.ON_RANK_CHANGED_COMMAND_ID = 300080008

    def fund_change(self, fund):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.FUND_CHANGE_COMMAND_ID, buffer)
        basic_codecs.IntCodec.encode(fund, buffer)
        self.space.send_command(self.game_object.id, buffer, "FUND_CHANGE")

    def round_finish(self, time_to_restart, user_infos):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.ROUND_FINISH_COMMAND_ID, buffer)
        basic_codecs.IntCodec.encode(time_to_restart, buffer)
        basic_codecs.VectorLevel1Codec.encode(user_infos, battle_codecs.UserRewardCodec, buffer)
        self.space.send_command(self.game_object.id, buffer, "ROUND_FINISH")

    def round_start(self, new_time_limit):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.ROUND_START_COMMAND_ID, buffer)
        basic_codecs.IntCodec.encode(new_time_limit, buffer)
        self.space.send_command(self.game_object.id, buffer, "ROUND_START")

    def on_rank_changed(self, user_id, rank_id):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.ON_RANK_CHANGED_COMMAND_ID, buffer)
        basic_codecs.LongCodec.encode(user_id, buffer)
        basic_codecs.ByteCodec.encode(rank_id, buffer)
        self.space.send_command(self.game_object.id, buffer, "ON_RANK_CHANGED")
