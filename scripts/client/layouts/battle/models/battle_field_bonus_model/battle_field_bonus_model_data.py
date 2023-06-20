from client.layouts.battle.models.battle_field_bonus_model import battle_field_bonus_model
from client.dispatcher.dispatcher_model import model_data
from client.layouts.battle import battle_codecs
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class BattleFieldBonusModelData:
    def __init__(self, game_object, battle_field_model_cc):
        self.game_object = game_object
        self.battle_field_model_cc = battle_field_model_cc

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.FloatCodec.encode(self.battle_field_model_cc.bonus_fall_speed, buffer)
        basic_codecs.VectorLevel1Codec.encode(self.battle_field_model_cc.bonuses, battle_codecs.BattleFieldBonusCodec, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = self.game_object.get_model(battle_field_bonus_model.BattleFieldBonusModel).model_id
        return _model_data
