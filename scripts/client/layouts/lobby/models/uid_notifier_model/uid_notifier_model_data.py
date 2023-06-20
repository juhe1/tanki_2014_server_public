from client.layouts.lobby.models.user_property_model import user_property_model
from client.dispatcher.dispatcher_model import model_data
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer
from . import uid_notifier_model

class UidNotifierModelData:
    def __init__(self, game_object, client_object):
        self.game_object = game_object

        self.uid = client_object.username
        self.user_id = client_object.user_id

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.StringCodec.encode(self.uid, buffer)
        basic_codecs.LongCodec.encode(self.user_id, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = self.game_object.get_model(uid_notifier_model.UidNotifierModel).model_id
        return _model_data
