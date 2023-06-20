from client.layouts.battle.models.statistics_dm_model import statistics_dm_model
from client.dispatcher.dispatcher_model import model_data
from client.layouts.battle import battle_codecs
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class StatisticsDmModelData:
    def __init__(self, game_object, user_infos):
        self.game_object = game_object

        self.user_infos = user_infos

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.VectorLevel1Codec.encode(self.user_infos, battle_codecs.UserInfoCodec, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = self.game_object.get_model(statistics_dm_model.StatisticsDmModel).model_id
        return _model_data
