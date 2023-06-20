from loaders.client_resource_loader import client_resource_loader
from client.layouts.battle.models.tank_model import tank_model
from client.dispatcher.dispatcher_model import model_data
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer
from . import smoky_shoot_sfx_model

class SmokyShootSfxModelData:
    def __init__(self, game_object, smoky_shoot_sfx_model_cc):
        self.game_object = game_object
        self.smoky_shoot_sfx_model_cc = smoky_shoot_sfx_model_cc

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.ShortCodec.encode(self.smoky_shoot_sfx_model_cc.critical_hit_size, buffer)
        basic_codecs.LongCodec.encode(self.smoky_shoot_sfx_model_cc.critical_hit_texture, buffer)
        basic_codecs.LongCodec.encode(self.smoky_shoot_sfx_model_cc.explosion_mark_texture, buffer)
        basic_codecs.ShortCodec.encode(self.smoky_shoot_sfx_model_cc.explosion_size, buffer)
        basic_codecs.LongCodec.encode(self.smoky_shoot_sfx_model_cc.explosion_sound, buffer)
        basic_codecs.LongCodec.encode(self.smoky_shoot_sfx_model_cc.explosion_texture, buffer)
        basic_codecs.LongCodec.encode(self.smoky_shoot_sfx_model_cc.shot_sound, buffer)
        basic_codecs.LongCodec.encode(self.smoky_shoot_sfx_model_cc.shot_texture, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = self.game_object.get_model(smoky_shoot_sfx_model.SmokyShootSfxModel).model_id
        return _model_data
