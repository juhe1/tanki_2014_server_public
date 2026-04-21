from loaders.server_properties_loader import server_properties_loader
from client.layouts.battle_list.models.battle_create_model import battle_create_model
from client.layouts.lobby.models.user_property_model import user_property_model
from client.layouts.battle_list.battle_create import rank_ranges
from client.layouts.battle_list import battle_list_codecs
from client.dispatcher.dispatcher_model import model_data
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer
from client.layouts.battle_list.battle_data import battle_limits

class BattleCreateModelData:
    def __init__(self, game_object, client_object):
        self.game_object = game_object

        _user_property_model = client_object.client_space_registry.get_model(user_property_model.UserPropertyModel, game_object_name="panel", space_name="lobby")

        self.battle_limits = [
            battle_limits.BattleLimits(server_properties_loader.properties.dm_battle_limit["score_limit"], server_properties_loader.properties.dm_battle_limit["time_limit_in_sec"]),
            battle_limits.BattleLimits(server_properties_loader.properties.tdm_battle_limit["score_limit"], server_properties_loader.properties.tdm_battle_limit["time_limit_in_sec"]),
            battle_limits.BattleLimits(server_properties_loader.properties.ctf_battle_limit["score_limit"], server_properties_loader.properties.ctf_battle_limit["time_limit_in_sec"]),
            battle_limits.BattleLimits(server_properties_loader.properties.cp_battle_limit["score_limit"], server_properties_loader.properties.cp_battle_limit["time_limit_in_sec"])
        ]

        self.battle_creation_disabled = False
        self.max_range_length = rank_ranges.get_range_by_rank_index(_user_property_model.model_data.rank)

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.BooleanCodec.encode(self.battle_creation_disabled, buffer)
        basic_codecs.VectorLevel1Codec.encode(self.battle_limits, battle_list_codecs.BattleLimitsCodec, buffer)
        basic_codecs.IntCodec.encode(self.max_range_length, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = self.game_object.get_model(battle_create_model.BattleCreateModel).model_id
        return _model_data
