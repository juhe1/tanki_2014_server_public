from client.dispatcher.dispatcher_model import model_data
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer
from . import flame_throwing_sfx_model

class FlameThrowingSfxModelData:
    def __init__(self, flame_throwing_sfx_model_cc):
        self.flame_throwing_sfx_model_cc = flame_throwing_sfx_model_cc

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.flame_throwing_sfx_model_cc.fire_texture, buffer)
        basic_codecs.LongCodec.encode(self.flame_throwing_sfx_model_cc.flame_sound, buffer)
        basic_codecs.LongCodec.encode(self.flame_throwing_sfx_model_cc.muzzle_plane_texture, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = flame_throwing_sfx_model.FlameThrowingSfxModel.model_id
        return _model_data
