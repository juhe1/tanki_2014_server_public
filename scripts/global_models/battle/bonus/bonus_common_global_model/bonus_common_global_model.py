from global_models.battle.common.battle_field_global_model import battle_field_global_model
from global_models.battle.common.battle_map_global_model import battle_map_global_model
from client.layouts.battle.models.bonus_common_model import bonus_common_model
from loaders.map_loader.map_info import BonusType
from space.global_model import GlobalModel
import server_properties

import random

class BonusCommonGlobalModel(GlobalModel):

    CLIENT_MODEL = bonus_common_model.BonusCommonModel

    def __init__(self, global_game_object, global_space, bonus_common_cc, bonus_type, owner_id=None):
        super().__init__(global_game_object, global_space, owner_id)

        self.bonus_type = bonus_type
        self.bonus_regions = self.get_bonus_regions(bonus_type)

        self.bonus_common_cc = bonus_common_cc
        self.bonus_common_cc.life_time = self.get_life_time()

    def get_life_time(self):
        if self.bonus_type == BonusType.ARMOR_BOX:
            return server_properties.ARMOR_BOX_LIFE_TIME_IN_SEC

        if self.bonus_type == BonusType.CRYSTAL_BOX:
            return server_properties.CRYSTAL_BOX_LIFE_TIME_IN_SEC

        if self.bonus_type == BonusType.GOLD_BOX:
            return server_properties.GOLD_BOX_LIFE_TIME_IN_SEC

        if self.bonus_type == BonusType.MED_BOX:
            return server_properties.MED_BOX_LIFE_TIME_IN_SEC

        if self.bonus_type == BonusType.NOS_BOX:
            return server_properties.NOS_BOX_LIFE_TIME_IN_SEC

        if self.bonus_type == BonusType.POWER_BOX:
            return server_properties.POWER_BOX_LIFE_TIME_IN_SEC

    def get_bonus_regions(self, bonus_type):
        map_info = self.global_space.get_global_model(battle_map_global_model.BattleMapGlobalModel, global_game_object_name="battle_map").map_info
        _battle_field_global_model = self.global_space.get_global_model(battle_field_global_model.BattleFieldGlobalModel, global_game_object_name="default_game_object")
        battle_info_global_model_data = _battle_field_global_model.battle_info_global_model_data

        return map_info.get_bonus_regions_by_battle_mode_and_bonus_type(battle_info_global_model_data.battle_mode, bonus_type)

    def generate_new_bonus_spawn_position(self):
        if self.bonus_regions == []: return
        random_bonus_region = random.choice(self.bonus_regions)
        return random_bonus_region.calculate_random_spawn_position()

    def get_model_data(self):
        return self.bonus_common_cc
