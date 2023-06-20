from client.layouts.battle.models.battle_field_model import battle_field_model
from client.dispatcher.dispatcher_model import model_data
from client.layouts.battle import battle_codecs
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class BattleFieldModelData:
    def __init__(self, game_object, client_object, global_model):
        self.game_object = game_object

        self.battle_field_model_cc = global_model.get_model_data()
        self.spectator = global_model.is_user_spectator(client_object.user_id)

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.BooleanCodec.encode(self.battle_field_model_cc.active, buffer)
        battle_codecs.BattleFieldSoundsCodec.encode(self.battle_field_model_cc.battlefield_sounds, buffer)
        basic_codecs.FloatCodec.encode(self.battle_field_model_cc.color_transform_multiplier, buffer)
        basic_codecs.IntCodec.encode(self.battle_field_model_cc.idle_kick_period_msec, buffer)
        basic_codecs.LongCodec.encode(self.battle_field_model_cc.map_game_object_id, buffer)
        basic_codecs.RangeCodec.encode(self.battle_field_model_cc.range, buffer)
        basic_codecs.FloatCodec.encode(self.battle_field_model_cc.shadow_map_correction_factor, buffer)
        basic_codecs.BooleanCodec.encode(self.spectator, buffer)
        basic_codecs.IntCodec.encode(self.battle_field_model_cc.tank_activation_delay_in_ms, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = self.game_object.get_model(battle_field_model.BattleFieldModel).model_id
        return _model_data
