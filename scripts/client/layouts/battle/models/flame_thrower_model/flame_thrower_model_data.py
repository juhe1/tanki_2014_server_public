from client.dispatcher.dispatcher_model import model_data
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer
from . import flame_thrower_model

class FlameThrowerModelData:
    def __init__(self, flame_thrower_model_cc):
        self.flame_thrower_model_cc = flame_thrower_model_cc

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.FloatCodec.encode(self.flame_thrower_model_cc.cone_angle, buffer)
        basic_codecs.FloatCodec.encode(self.flame_thrower_model_cc.range, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = flame_thrower_model.FlameThrowerModel.model_id
        return _model_data
