from client.dispatcher.dispatcher_model import model_data
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer
from . import example_model

class ExampleModelData:
    def __init__(self):
        self.example_property = True

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.BooleanCodec.encode(self.example_property, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = example_model.ExampleModel.model_id
        return _model_data
