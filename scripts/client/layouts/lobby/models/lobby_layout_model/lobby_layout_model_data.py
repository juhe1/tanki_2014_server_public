from client.layouts.lobby.models.lobby_layout_model import lobby_layout_model
from client.dispatcher.dispatcher_model import model_data
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer
import server_properties

class LobbyLayoutModelData:
    def __init__(self, game_object):
        self.game_object = game_object
        self.disable_payment = server_properties.DISABLE_PAYMENT

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.BooleanCodec.encode(self.disable_payment, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = self.game_object.get_model(lobby_layout_model.LobbyLayoutModel).model_id
        return _model_data
