from client.layouts.lobby.models.user_property_model import user_property_model
from client.dispatcher.dispatcher_model import model_data
from utils.binary.codecs import basic_codecs
from . import user_email_and_password_model
from utils.binary import binary_buffer


class UserEmailAndPasswordModelData:
    def __init__(self, game_object, client_object):
        self.game_object = game_object
        self.user_property_model = game_object.get_model(user_property_model.UserPropertyModel)

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.OptionalCodec.encode((self.user_property_model.model_data.email, buffer), buffer, basic_codecs.StringCodec)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = self.game_object.get_model(user_email_and_password_model.UserEmailAndPasswordModel).model_id
        return _model_data
