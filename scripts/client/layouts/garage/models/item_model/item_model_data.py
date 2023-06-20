from loaders.client_resource_loader import client_resource_loader
from client.layouts.garage.models.item_model import item_model
from client.dispatcher.dispatcher_model import model_data
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class ItemModelData:
    def __init__(self, game_object, client_object, garage_item_object):
        self.garage_item_object = garage_item_object
        self.game_object = game_object

        self.min_rank = self.garage_item_object.min_rank
        self.max_rank = self.garage_item_object.max_rank
        self.position = self.garage_item_object.position
        self.preview_image = client_resource_loader.get_resource_id(self.garage_item_object.preview_image)

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.IntCodec.encode(self.max_rank, buffer)
        basic_codecs.IntCodec.encode(self.min_rank, buffer)
        basic_codecs.ShortCodec.encode(self.position, buffer)
        basic_codecs.LongCodec.encode(self.preview_image, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = self.game_object.get_model(item_model.ItemModel).model_id
        return _model_data
