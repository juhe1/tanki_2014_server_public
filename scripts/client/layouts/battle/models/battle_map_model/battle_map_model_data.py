from client.layouts.battle.models.battle_map_model import battle_map_model
from loaders.graphics_settings_loader import graphics_settings_loader
from loaders.client_resource_loader import client_resource_loader
from client.dispatcher.dispatcher_model import model_data
from client.layouts.battle import battle_codecs
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class BattleMapModelData:
    def __init__(self, game_object, client_object, battle_map_model_cc):
        self.game_object = game_object
        self.battle_map_model_cc = battle_map_model_cc

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        battle_codecs.DustParamsCodec.encode(self.battle_map_model_cc.dust_params, buffer)
        battle_codecs.DynamicShadowParamsCodec.encode(self.battle_map_model_cc.dynamic_shadow_params, buffer)
        basic_codecs.LongCodec.encode(self.battle_map_model_cc.environment_sound_resource_id, buffer)
        battle_codecs.FogParamsCodec.encode(self.battle_map_model_cc.fog_params, buffer)
        basic_codecs.FloatCodec.encode(self.battle_map_model_cc.gravity, buffer)
        basic_codecs.LongCodec.encode(self.battle_map_model_cc.map_resource_id, buffer)
        basic_codecs.Vector3DCodec.encode(self.battle_map_model_cc.sky_box_revolution_axis, buffer)
        basic_codecs.FloatCodec.encode(self.battle_map_model_cc.sky_box_revolution_speed, buffer)
        basic_codecs.LongCodec.encode(self.battle_map_model_cc.sky_box_resource_id, buffer)
        basic_codecs.IntCodec.encode(self.battle_map_model_cc.ssao_color, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = self.game_object.get_model(battle_map_model.BattleMapModel).model_id
        return _model_data
