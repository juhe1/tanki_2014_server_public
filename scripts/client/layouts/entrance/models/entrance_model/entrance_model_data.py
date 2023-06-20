from client.layouts.entrance.models.entrance_model import entrance_model
from client.dispatcher.dispatcher_model import model_data
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer
import server_properties

class EntranceModelData:
    def __init__(self, game_object, client_object):
        self.game_object = game_object

        self.anti_addiction_enabled = False
        self.in_game_registration = server_properties.IN_GAME_REGISTRATION

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.BooleanCodec.encode(self.anti_addiction_enabled, buffer)
        basic_codecs.BooleanCodec.encode(self.in_game_registration, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = self.game_object.get_model(entrance_model.EntranceModel).model_id
        return _model_data
