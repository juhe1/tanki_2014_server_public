from client.layouts.battle.models.bcsh_model import bcsh_model
from client.dispatcher.dispatcher_model import model_data
from client.layouts.battle import battle_codecs
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class BcshModelData:
    def __init__(self, game_object, bcsh_model_cc):
        self.game_object = game_object
        self.bcsh_data = bcsh_model_cc.bcsh_data

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.VectorLevel1Codec.encode(self.bcsh_data, battle_codecs.BCSHStructCodec, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = self.game_object.get_model(bcsh_model.BcshModel).model_id
        return _model_data
