from client.dispatcher.dispatcher_model import model_data
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer
from . import data_owner_model

class DataOwnerModelData:
    def __init__(self, game_object, data_owner_id):
        self.game_object = game_object
        self.data_owner_id = data_owner_id

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.data_owner_id, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = self.game_object.get_model(data_owner_model.DataOwnerModel).model_id
        return _model_data
