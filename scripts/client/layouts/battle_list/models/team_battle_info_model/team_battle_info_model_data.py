from client.layouts.battle_list.models.team_battle_info_model import team_battle_info_model
from client.layouts.battle_list import battle_list_codecs
from client.dispatcher.dispatcher_model import model_data
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class TeamBattleInfoModelData:
    def __init__(self, game_object, team_battle_info_model_cc):
        self.game_object = game_object
        self.team_battle_info_model_cc = team_battle_info_model_cc

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.BooleanCodec.encode(self.team_battle_info_model_cc.auto_balance, buffer)
        basic_codecs.BooleanCodec.encode(self.team_battle_info_model_cc.friendly_fire, buffer)
        basic_codecs.IntCodec.encode(self.team_battle_info_model_cc.blue_score, buffer)
        basic_codecs.IntCodec.encode(self.team_battle_info_model_cc.red_score, buffer)
        basic_codecs.VectorLevel1Codec.encode(self.team_battle_info_model_cc.blue_user_infos, battle_list_codecs.BattleInfoUserCodec, buffer)
        basic_codecs.VectorLevel1Codec.encode(self.team_battle_info_model_cc.red_user_infos, battle_list_codecs.BattleInfoUserCodec, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = self.game_object.get_model(team_battle_info_model.TeamBattleInfoModel).model_id
        return _model_data
