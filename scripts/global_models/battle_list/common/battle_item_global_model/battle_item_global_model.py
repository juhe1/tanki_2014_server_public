from global_models.battle_list.dm.battle_dm_item_global_model import battle_dm_item_global_model
from global_models.battle_list.dm.battle_dm_info_global_model import battle_dm_info_global_model
from global_models.battle_list.team.team_battle_item_global_model import team_battle_item_global_model
from global_models.battle_list.team.team_battle_info_global_model import team_battle_info_global_model
from global_models.battle_list.common.battle_select_global_model import battle_select_global_model
from global_models.battle_list.common.battle_info_global_model import battle_info_global_model
from global_models.battle.common.battle_field_global_model import battle_field_global_model
from global_models.battle_list.common.battle_info_global_model import battle_info_model_cc
from client.layouts.battle_list.models.battle_item_model import battle_item_model
from global_models.battle.common.chat_global_model import chat_global_model
from client.layouts.battle_list.battle_data.battle_mode import BattleMode
from space.global_model import GlobalModel
from space import global_space_registry
from . import battle_item_model_cc

BATTLE_SPACE_ID_OFFSET = 200

class BattleItemGlobalModel(GlobalModel):

    CLIENT_MODEL = battle_item_model.BattleItemModel

    def __init__(self, global_game_object, global_space, battle_data, owner_id=None):
        super().__init__(global_game_object, global_space, owner_id)

        self.battle_select_model = global_space.get_global_model(battle_select_global_model.BattleSelectGlobalModel, global_game_object_name="default_game_object")
        self.battle_item_model_cc = self.create_battle_item_model_cc(battle_data)

        self.allowed_private_battle_user_names = [] # usernames of users that are allowd to connect into this battle

        if battle_data.private_battle:
            self.allowed_private_battle_user_names.append(battle_data.battle_creator_client_object.username)

        self.battle_info_global_game_object = self.create_battle_info_global_game_object(battle_data)
        self.battle_field_global_space = None
        self.battle_field_global_game_object = self.create_battle_field_global_game_object(battle_data.battle_id)

    def create_battle_field_global_game_object(self, battle_id):
        battle_field_space_global_id = battle_id + BATTLE_SPACE_ID_OFFSET
        self.battle_field_global_space = global_space_registry.add_space(id=battle_field_space_global_id, name="battle_field_" + str(battle_id))

        battle_field_global_game_object = self.battle_field_global_space.get_default_global_game_object()
        battle_field_global_game_object.add_global_model(battle_field_global_model.BattleFieldGlobalModel, model_args=(self,))
        battle_field_global_game_object.add_global_model(chat_global_model.ChatGlobalModel)

        return battle_field_global_game_object

    def create_battle_item_model_cc(self, battle_data):
        _battle_item_model_cc = battle_item_model_cc.BattleItemModelCC()
        _battle_item_model_cc.battle_id = battle_data.battle_id
        _battle_item_model_cc.battle_mode = battle_data.battle_mode
        _battle_item_model_cc.max_people_count = battle_data.max_people_count
        _battle_item_model_cc.name = battle_data.name
        _battle_item_model_cc.without_supplies = battle_data.without_supplies
        _battle_item_model_cc.private_battle = battle_data.private_battle
        _battle_item_model_cc.pro_battle = battle_data.pro_battle
        _battle_item_model_cc.rank_range = battle_data.rank_range
        _battle_item_model_cc.suspicious = False # TODO: get suspicious somewhere
        _battle_item_model_cc.map_game_object_id = self.battle_select_model.get_map_global_game_object_by_id(battle_data.map_id).id
        return _battle_item_model_cc

    def is_user_allowed_to_join(self, username):
        return (self.battle_item_model_cc.private_battle == False) or (username in self.allowed_private_battle_user_names)

    def add_battle_mode_specifig_models(self, battle_mode, battle_info_global_game_object, battle_data):
        if battle_mode == BattleMode.DM:
            _battle_dm_info_global_model = battle_info_global_game_object.add_global_model(battle_dm_info_global_model.BattleDmInfoGlobalModel, model_args=(self,))
            self.global_game_object.add_global_model(battle_dm_item_global_model.BattleDmItemGlobalModel, model_args=(_battle_dm_info_global_model,))
            return

        if battle_mode in [BattleMode.TDM, BattleMode.CTF, BattleMode.CP]:
            _team_battle_info_global_model = battle_info_global_game_object.add_global_model(team_battle_info_global_model.TeamBattleInfoGlobalModel, model_args=(self, battle_data))
            self.global_game_object.add_global_model(team_battle_item_global_model.TeamBattleItemGlobalModel, model_args=(_team_battle_info_global_model,))

    def create_battle_info_global_game_object(self, battle_data):
        _battle_info_model_cc = battle_info_model_cc.BattleInfoModelCC()
        _battle_info_model_cc.battle_mode = self.battle_item_model_cc.battle_mode
        _battle_info_model_cc.battle_id = self.battle_item_model_cc.battle_id
        _battle_info_model_cc.limits = battle_data.limits
        _battle_info_model_cc.map_game_object_id = self.battle_item_model_cc.map_game_object_id
        _battle_info_model_cc.max_people_count = self.battle_item_model_cc.max_people_count
        _battle_info_model_cc.name = self.battle_item_model_cc.name
        _battle_info_model_cc.pro_battle = self.battle_item_model_cc.pro_battle
        _battle_info_model_cc.rank_range = self.battle_item_model_cc.rank_range
        _battle_info_model_cc.without_bonuses = battle_data.without_bonuses
        _battle_info_model_cc.without_crystals = battle_data.without_crystals
        _battle_info_model_cc.without_supplies = self.battle_item_model_cc.without_supplies
        _battle_info_model_cc.without_upgrades = battle_data.without_upgrades

        battle_info_global_game_object = self.global_space.add_global_game_object("battle_info_" + str(battle_data.battle_id))

        self.add_battle_mode_specifig_models(battle_data.battle_mode, battle_info_global_game_object, battle_data)

        battle_info_global_game_object.add_global_model(battle_info_global_model.BattleInfoGlobalModel, model_args=(_battle_info_model_cc, self,))
        return battle_info_global_game_object

    def get_model_data(self):
        return self.battle_item_model_cc
