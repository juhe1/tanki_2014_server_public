from client.layouts.lobby.models.user_property_model import user_property_model
from client.dispatcher.dispatcher_model import model_data
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer
from . import rank_notifier_model

class RankNotifierModelData:
    def __init__(self, game_object, client_object):
        self.game_object = game_object
        self.client_object = client_object

    def get_model_data(self):
        user_property_model_data = self.client_object.client_space_registry.get_model(user_property_model.UserPropertyModel, game_object_name="panel", space_name="lobby").model_data
        self.rank = user_property_model_data.rank
        self.user_id = user_property_model_data.user_id

        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.IntCodec.encode(self.rank, buffer)
        basic_codecs.LongCodec.encode(self.user_id, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = self.game_object.get_model(rank_notifier_model.RankNotifierModel).model_id
        return _model_data
