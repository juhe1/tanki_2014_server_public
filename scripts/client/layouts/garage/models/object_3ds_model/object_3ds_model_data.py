from client.layouts.garage.models.object_3ds_model import object_3ds_model
from loaders.client_resource_loader import client_resource_loader
from client.dispatcher.dispatcher_model import model_data
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer


class Object3DSModelData:
    def __init__(self, game_object, client_object, _3ds_resource_name):
        self.game_object = game_object
        self.resource_id = client_resource_loader.get_resource_id(_3ds_resource_name)

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.resource_id, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = self.game_object.get_model(object_3ds_model.Object3DSModel).model_id
        return _model_data
