from client.layouts.battle_list.models.battle_dm_info_model import battle_dm_info_model
from client.layouts.battle_list import battle_list_codecs
from client.dispatcher.dispatcher_model import model_data
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class BattleDmInfoModelData:
    def __init__(self, game_object, battle_dm_info_model_cc):
        self.game_object = game_object
        self.battle_dm_info_model_cc = battle_dm_info_model_cc

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.VectorLevel1Codec.encode(self.battle_dm_info_model_cc.user_infos, battle_list_codecs.BattleInfoUserCodec, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = self.game_object.get_model(battle_dm_info_model.BattleDmInfoModel).model_id
        return _model_data
