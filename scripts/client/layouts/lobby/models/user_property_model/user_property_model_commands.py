from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class UserPropertyModelCommands:
    def __init__(self, space, game_object):
        self.space = space
        self.game_object = game_object
        self.CHANGE_CRYSTAL_COMMAND_ID = 300050062
        self.UPDATE_RANK_COMMAND_ID = 300050063
        self.UPDATE_RATING_AND_PLACE_COMMAND_ID = 300050064
        self.UPDATE_SCORE_COMMAND_ID = 300050065

    def change_crystal(self, crystals):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.CHANGE_CRYSTAL_COMMAND_ID, buffer)
        basic_codecs.IntCodec.encode(crystals, buffer)
        self.space.send_command(self.game_object.id, buffer, "CHANGE_CRYSTAL")

    def update_score(self, score):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.UPDATE_SCORE_COMMAND_ID, buffer)
        basic_codecs.IntCodec.encode(score, buffer)
        self.space.send_command(self.game_object.id, buffer, "UPDATE_SCORE")

    def update_rank(self, new_rank, score, current_rank_score, next_rank_score, bonus_crystals):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.UPDATE_RANK_COMMAND_ID, buffer)
        basic_codecs.ByteCodec.encode(new_rank, buffer)
        basic_codecs.IntCodec.encode(score, buffer)
        basic_codecs.IntCodec.encode(current_rank_score, buffer)
        basic_codecs.IntCodec.encode(next_rank_score, buffer)
        basic_codecs.IntCodec.encode(bonus_crystals, buffer)
        self.space.send_command(self.game_object.id, buffer, "UPDATE_RANK")
