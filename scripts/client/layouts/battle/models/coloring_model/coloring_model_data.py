from loaders.client_resource_loader import client_resource_loader
from client.dispatcher.dispatcher_model import model_data
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer
from . import coloring_model

class ColoringModelData:
    def __init__(self, game_object, color_resource_name):
        self.game_object = game_object
        self.coloring_image_id = client_resource_loader.get_resource_id(color_resource_name)

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.coloring_image_id, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = self.game_object.get_model(coloring_model.ColoringModel).model_id
        return _model_data
