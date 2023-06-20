from client.layouts.battle_list.models.battle_create_model import battle_create_model
from client.layouts.battle_list.models.battle_info_model import battle_info_model
from client.layouts.lobby.models.user_property_model import user_property_model
from client.layouts.lobby.lobby_enums import UserRole
from client.dispatcher.dispatcher_model import model_data
from client.layouts.battle_list import battle_list_codecs
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class BattleInfoModelData:
    def __init__(self, game_object, client_object, space, battle_info_model_cc):
        self.game_object = game_object
        self.space = space

        _battle_create_model = self.space.get_model(battle_create_model.BattleCreateModel, "default_game_object")
        _user_property_model = client_object.client_space_registry.get_model(user_property_model.UserPropertyModel, game_object_name="panel", space_name="lobby")

        self.battle_info_model_cc = battle_info_model_cc
        battle_info_model_cc.user_paid = False # TODO: get user_paid
        battle_info_model_cc.spectator = _user_property_model.model_data.user_owns_role(UserRole.SPECTATOR)

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        battle_list_codecs.BattleModeCodec.encode(self.battle_info_model_cc.battle_mode, buffer)
        basic_codecs.LongCodec.encode(self.battle_info_model_cc.battle_id, buffer)
        battle_list_codecs.BattleLimitsCodec.encode(self.battle_info_model_cc.limits, buffer)
        basic_codecs.LongCodec.encode(self.battle_info_model_cc.map_game_object_id, buffer)
        basic_codecs.ByteCodec.encode(self.battle_info_model_cc.max_people_count, buffer)
        basic_codecs.StringCodec.encode(self.battle_info_model_cc.name, buffer)
        basic_codecs.BooleanCodec.encode(self.battle_info_model_cc.pro_battle, buffer)
        basic_codecs.RangeCodec.encode(self.battle_info_model_cc.rank_range, buffer)
        basic_codecs.BooleanCodec.encode(self.battle_info_model_cc.round_started, buffer)
        basic_codecs.BooleanCodec.encode(self.battle_info_model_cc.spectator, buffer)
        basic_codecs.IntCodec.encode(self.battle_info_model_cc.time_left_in_seconds, buffer)
        basic_codecs.BooleanCodec.encode(self.battle_info_model_cc.user_paid, buffer)
        basic_codecs.BooleanCodec.encode(self.battle_info_model_cc.without_bonuses, buffer)
        basic_codecs.BooleanCodec.encode(self.battle_info_model_cc.without_crystals, buffer)
        basic_codecs.BooleanCodec.encode(self.battle_info_model_cc.without_supplies, buffer)
        basic_codecs.BooleanCodec.encode(self.battle_info_model_cc.without_upgrades, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = self.game_object.get_model(battle_info_model.BattleInfoModel).model_id
        return _model_data
