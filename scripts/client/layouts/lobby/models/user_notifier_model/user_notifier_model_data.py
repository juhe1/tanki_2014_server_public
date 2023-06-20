from client.dispatcher.dispatcher_model import model_data
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer
from . import user_notifier_model

class UserNotifierModelData:
    def __init__(self, game_object, client_object):
        self.game_object = game_object
        self.client_object = client_object

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.client_object.user_id, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = self.game_object.get_model(user_notifier_model.UserNotifierModel).model_id
        return _model_data
