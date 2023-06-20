from client.layouts.garage.models.description_model import description_model
from client.dispatcher.dispatcher_model import model_data
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class DescriptionModelData:
    def __init__(self, game_object, client_object, garage_item_object):
        self.garage_item_object = garage_item_object
        self.game_object = game_object

        self.description = garage_item_object.description
        self.name = garage_item_object.name

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.OptionalCodec.encode((self.description, buffer), buffer, basic_codecs.StringCodec)
        basic_codecs.OptionalCodec.encode((self.name, buffer), buffer, basic_codecs.StringCodec)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = self.game_object.get_model(description_model.DescriptionModel).model_id
        return _model_data
