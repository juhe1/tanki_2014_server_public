from client.dispatcher.dispatcher_model import model_data
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer
from . import shaft_shoot_sfx_model

class ShaftShootSfxModelData:
    def __init__(self, shaft_shoot_sfx_model_cc):
        self.shaft_shoot_sfx_model_cc = shaft_shoot_sfx_model_cc

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.shaft_shoot_sfx_model_cc.explosion_sound, buffer)
        basic_codecs.LongCodec.encode(self.shaft_shoot_sfx_model_cc.explosion_texture, buffer)
        basic_codecs.LongCodec.encode(self.shaft_shoot_sfx_model_cc.hit_mark_texture, buffer)
        basic_codecs.LongCodec.encode(self.shaft_shoot_sfx_model_cc.muzzle_flash_texture, buffer)
        basic_codecs.LongCodec.encode(self.shaft_shoot_sfx_model_cc.shot_sound, buffer)
        basic_codecs.LongCodec.encode(self.shaft_shoot_sfx_model_cc.targeting_sound, buffer)
        basic_codecs.LongCodec.encode(self.shaft_shoot_sfx_model_cc.trail_texture, buffer)
        basic_codecs.LongCodec.encode(self.shaft_shoot_sfx_model_cc.zoom_mode_sound, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = shaft_shoot_sfx_model.ShaftShootSfxModel.model_id
        return _model_data
