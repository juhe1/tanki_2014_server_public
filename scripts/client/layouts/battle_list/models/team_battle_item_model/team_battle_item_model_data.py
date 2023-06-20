from client.layouts.battle_list.models.team_battle_item_model import team_battle_item_model
from client.layouts.lobby.models.user_property_model import user_property_model
from client.dispatcher.dispatcher_model import model_data
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class TeamBattleItemModelData:
    def __init__(self, game_object, team_battle_item_model_cc):
        self.game_object = game_object
        self.team_battle_item_model_cc = team_battle_item_model_cc

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.VectorLevel1Codec.encode(self.team_battle_item_model_cc.blue_user_ids, basic_codecs.LongCodec, buffer)
        basic_codecs.VectorLevel1Codec.encode(self.team_battle_item_model_cc.red_user_ids, basic_codecs.LongCodec, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = self.game_object.get_model(team_battle_item_model.TeamBattleItemModel).model_id
        return _model_data
