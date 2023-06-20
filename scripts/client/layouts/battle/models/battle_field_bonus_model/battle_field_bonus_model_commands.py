from client.layouts.battle import battle_codecs
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class BattleFieldBonusModelCommands:
    def __init__(self, space, game_object):
        self.space = space
        self.game_object = game_object

        self.BONUS_TAKEN_COMMAND_ID = 300100006
        self.GOLD_TAKEN_COMMAND_ID = 300100007
        self.HOLIDAY_CRYSTAL_TAKEN_COMMAND_ID = 300100008
        self.REMOVE_BONUSES_COMMAND_ID = 300100009
        self.SPAWN_BONUSES_COMMAND_ID = 300100010

    def bonus_taken(self, bonus_id):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.BONUS_TAKEN_COMMAND_ID, buffer)
        basic_codecs.LongCodec.encode(bonus_id, buffer)
        basic_codecs.LongCodec.encode(345346456, buffer) # this -> "345346456" is just some random shit, because it is not used in the client code
        self.space.send_command(self.game_object.id, buffer, "BONUS_TAKEN")

    def gold_taken(self, taker_user_id):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.GOLD_TAKEN_COMMAND_ID, buffer)
        basic_codecs.LongCodec.encode(taker_user_id, buffer)
        self.space.send_command(self.game_object.id, buffer, "GOLD_TAKEN")

    def holiday_crystal_taken(self, taker_user_id):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.HOLIDAY_CRYSTAL_TAKEN_COMMAND_ID, buffer)
        basic_codecs.LongCodec.encode(taker_user_id, buffer)
        self.space.send_command(self.game_object.id, buffer, "HOLIDAY_CRYSTAL_TAKEN")

    def remove_bonuses(self, bonus_ids):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.REMOVE_BONUSES_COMMAND_ID, buffer)
        basic_codecs.VectorLevel1Codec.encode(bonus_ids, basic_codecs.LongCodec, buffer)
        self.space.send_command(self.game_object.id, buffer, "REMOVE_BONUSES")

    def spawn_bonuses(self, bonuses):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.SPAWN_BONUSES_COMMAND_ID, buffer)
        basic_codecs.VectorLevel1Codec.encode(bonuses, battle_codecs.BattleFieldBonusSpawnCodec, buffer)
        self.space.send_command(self.game_object.id, buffer, "SPAWN_BONUSES")
