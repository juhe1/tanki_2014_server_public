from client.dispatcher.dispatcher_model import model_data
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer
from . import freeze_model

class FreezeModelData:
    def __init__(self, freeze_model_cc):
        self.freeze_model_cc = freeze_model_cc

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.FloatCodec.encode(self.freeze_model_cc.cone_angle, buffer)
        basic_codecs.FloatCodec.encode(self.freeze_model_cc.range, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = freeze_model.FreezeModel.model_id
        return _model_data
