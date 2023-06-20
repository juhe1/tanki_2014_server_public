from client.dispatcher.dispatcher_model import model_data
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer
from . import duration_controller_model

class DurationControllerModelData:
    def __init__(self, time_left_in_ms):
        self.time_left_in_ms = time_left_in_ms

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.IntCodec.encode(self.time_left_in_ms, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = duration_controller_model.DurationControllerModel.model_id
        return _model_data
