from client.layouts.garage.models.discount_model import discount_model
from loaders.client_resource_loader import client_resource_loader
from client.dispatcher.dispatcher_model import model_data
from client.layouts.garage import garage_codecs
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class DiscountModelData:
    def __init__(self, game_object, client_object, garage_item_object):
        self.garage_item_object = garage_item_object
        self.game_object = game_object

        self.discount = garage_item_object.discount

        self.image = None
        if garage_item_object.discount_image != None:
            self.image = client_resource_loader.get_resource_id(garage_item_object.discount_image)

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.FloatCodec.encode(self.discount * 100, buffer)
        basic_codecs.OptionalCodec.encode((self.image, buffer), buffer, basic_codecs.LongCodec)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = self.game_object.get_model(discount_model.DiscountModel).model_id
        return _model_data
