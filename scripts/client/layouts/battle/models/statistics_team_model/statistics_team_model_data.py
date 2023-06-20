from client.layouts.battle import battle_codecs
from client.dispatcher.dispatcher_model import model_data
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer
from . import statistics_team_model

class StatisticsTeamModelData:
    def __init__(self, statistics_model_cc):
        self.statistics_model_cc = statistics_model_cc

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.IntCodec.encode(self.statistics_model_cc.score_blue, buffer)
        basic_codecs.IntCodec.encode(self.statistics_model_cc.score_red, buffer)
        basic_codecs.VectorLevel1Codec.encode(self.statistics_model_cc.blue_user_infos, battle_codecs.UserInfoCodec, buffer)
        basic_codecs.VectorLevel1Codec.encode(self.statistics_model_cc.red_user_infos, battle_codecs.UserInfoCodec, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = statistics_team_model.StatisticsTeamModel.model_id
        return _model_data
