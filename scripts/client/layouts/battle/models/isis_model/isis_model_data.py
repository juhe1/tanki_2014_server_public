from client.dispatcher.dispatcher_model import model_data
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer
from . import isis_model

class IsisModelData:
    def __init__(self, isis_model_cc):
        self.isis_model_cc = isis_model_cc

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.BooleanCodec.encode(self.isis_property, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = isis_model.IsisModel.model_id
        return _model_data
