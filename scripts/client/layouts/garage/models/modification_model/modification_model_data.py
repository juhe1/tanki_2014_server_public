from client.layouts.garage.models.modification_model import modification_model
from client.dispatcher.dispatcher_model import model_data
from client.layouts.garage import garage_codecs
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class ModificationModelData:
    def __init__(self, game_object, client_object, garage_item_object):
        self.garage_item_object = garage_item_object
        self.game_object = game_object

        self.base_item_id = garage_item_object.base_item_id
        self.modification_index = garage_item_object.modification_index

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.base_item_id, buffer)
        basic_codecs.ByteCodec.encode(self.modification_index, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = self.game_object.get_model(modification_model.ModificationModel).model_id
        return _model_data
