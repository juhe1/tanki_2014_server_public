from client.layouts.garage.models.garage_model import garage_model
from loaders.client_resource_loader import client_resource_loader
from client.dispatcher.dispatcher_model import model_data
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class GarageModelData:
    def __init__(self, game_object, client_object):
        self.game_object = game_object
        self.client_object = client_object
        self.garage_box_resource = None

    def get_model_data(self):
        self.garage_box_resource = client_resource_loader.get_resource_id("/garage/3ds/garage_box")

        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.garage_box_resource, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = self.game_object.get_model(garage_model.GarageModel).model_id
        return _model_data
