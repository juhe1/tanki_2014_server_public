from client.layouts.battle_list.models.battle_create_model import battle_create_model
from client.layouts.lobby.models.user_property_model import user_property_model
from client.layouts.battle_list.battle_create import rank_ranges
from client.layouts.battle_list import battle_list_codecs
from client.dispatcher.dispatcher_model import model_data
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer
import server_properties

class BattleCreateModelData:
    def __init__(self, game_object, client_object):
        self.game_object = game_object

        _user_property_model = client_object.client_space_registry.get_model(user_property_model.UserPropertyModel, game_object_name="panel", space_name="lobby")

        self.battle_limits = [
            server_properties.DM_BATTLE_LIMIT,
            server_properties.TDM_BATTLE_LIMIT,
            server_properties.CTF_BATTLE_LIMIT,
            server_properties.CP_BATTLE_LIMIT
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
