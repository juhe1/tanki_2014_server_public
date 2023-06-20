from client.dispatcher.dispatcher_model import model_data
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer
from . import freeze_sfx_model

class FreezeSfxModelData:
    def __init__(self, freeze_sfx_model_cc):
        self.freeze_sfx_model_cc = freeze_sfx_model_cc

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.FloatCodec.encode(self.freeze_sfx_model_cc.particle_speed, buffer)
        basic_codecs.LongCodec.encode(self.freeze_sfx_model_cc.particle_texture, buffer)
        basic_codecs.LongCodec.encode(self.freeze_sfx_model_cc.plane_texture, buffer)
        basic_codecs.LongCodec.encode(self.freeze_sfx_model_cc.shot_sound, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = freeze_sfx_model.FreezeSfxModel.model_id
        return _model_data
