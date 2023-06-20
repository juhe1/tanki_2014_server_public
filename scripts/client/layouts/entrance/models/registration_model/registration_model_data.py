from client.layouts.entrance.models.registration_model import registration_model
from loaders.client_resource_loader import client_resource_loader
from client.dispatcher.dispatcher_model import model_data
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer
import server_properties

class RegistrationModelData:
    def __init__(self, game_object, client_object):
        self.game_object = game_object

        self.background_resource = client_resource_loader.get_resource_id("/entrance/images/background")
        self.enable_required_email = server_properties.ENABLE_REQUIRED_EMAIL
        self.max_password_length = server_properties.MAX_PASSWORD_LENGTH
        self.min_password_length = server_properties.MIN_PASSWORD_LENGTH

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.background_resource, buffer)
        basic_codecs.BooleanCodec.encode(self.enable_required_email, buffer)
        basic_codecs.IntCodec.encode(self.max_password_length, buffer)
        basic_codecs.IntCodec.encode(self.min_password_length, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = self.game_object.get_model(registration_model.RegistrationModel).model_id
        return _model_data
