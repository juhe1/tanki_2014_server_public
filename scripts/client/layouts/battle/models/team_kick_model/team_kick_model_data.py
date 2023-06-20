from client.dispatcher.dispatcher_model import model_data
from client.layouts.battle import battle_codecs
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer
from . import team_kick_model

class TeamKickModelData:
    def __init__(self, team_kick_model_cc):
        self.team_kick_model_cc = team_kick_model_cc

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.VectorLevel1Codec.encode(self.team_kick_model_cc.allys, battle_codecs.UserTeamKickDataCodec, buffer)
        battle_codecs.UserTeamKickDataCodec.encode(self.team_kick_model_cc.current_user, buffer)
        basic_codecs.BooleanCodec.encode(self.team_kick_model_cc.disabled, buffer)
        basic_codecs.IntCodec.encode(self.team_kick_model_cc.duration_immunity_affter_enter_in_sec, buffer)
        basic_codecs.IntCodec.encode(self.team_kick_model_cc.enter_time_diff_in_sec, buffer)
        basic_codecs.IntCodec.encode(self.team_kick_model_cc.immunity_stay_in_battle_in_sec, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = team_kick_model.TeamKickModel.model_id
        return _model_data
