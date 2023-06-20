from client.layouts.battle.models.statistics_model import statistics_model
from client.layouts.battle_list import battle_list_codecs
from client.dispatcher.dispatcher_model import model_data
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class StatisticsModelData:
    def __init__(self, game_object, client_object, global_model):
        self.game_object = game_object

        self.statistics_model_cc = global_model.get_model_data()
        self.statistics_model_cc.spectator = global_model.is_user_spectator(client_object.user_id)

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.StringCodec.encode(self.statistics_model_cc.battle_name, buffer)
        basic_codecs.IntCodec.encode(self.statistics_model_cc.fund, buffer)
        battle_list_codecs.BattleLimitsCodec.encode(self.statistics_model_cc.limits, buffer)
        basic_codecs.IntCodec.encode(self.statistics_model_cc.max_people_count, buffer)
        basic_codecs.BooleanCodec.encode(self.statistics_model_cc.spectator, buffer)
        basic_codecs.VectorLevel1Codec.encode(self.statistics_model_cc.suspicious_user_ids, basic_codecs.LongCodec, buffer)
        basic_codecs.IntCodec.encode(self.statistics_model_cc.time_left, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = self.game_object.get_model(statistics_model.StatisticsModel).model_id
        return _model_data
