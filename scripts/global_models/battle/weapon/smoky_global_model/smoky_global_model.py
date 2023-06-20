from global_models.battle.weapon.weapon_common_global_model import weapon_common_global_model
from global_models.battle.common.tank_global_model.tank_state import LogicStateEnum
from global_models.battle.common.tank_global_model import tank_global_model
from global_models.battle.weapon.smoky_shoot_sfx_global_model import smoky_shoot_sfx_global_model
from client.layouts.battle.models.smoky_model import smoky_model
from space.global_model import GlobalModel
from utils.time.timer import Timer
import server_properties

import random

TURRET_PROTECTION_NAME = "smoky_resistance"

class SmokyGlobalModel(GlobalModel):

    CLIENT_MODEL = smoky_model.SmokyModel

    def __init__(self, global_game_object, global_space, turret_database_item, owner_id=None):
        super().__init__(global_game_object, global_space, owner_id)

        # create sfx model
        turret_garage_item = turret_database_item.garage_item
        global_game_object.add_global_model(smoky_shoot_sfx_global_model.SmokyShootSfxGlobalModel, model_args=(turret_garage_item,))

        self.weapon_common_global_model = global_game_object.get_global_model(weapon_common_global_model.WeaponCommonGlobalModel)
        self.min_damage = turret_database_item.get_property_value("damage_to")
        self.max_damage = turret_database_item.get_property_value("damage_from")
        self.critical_hit_chance = turret_database_item.get_property_value("critical_hit_chance")
        self.critical_hit_damage = turret_database_item.get_property_value("critical_hit_damage")
        cooldown = turret_database_item.get_property_value("weapon_reload_time")

        self.shoot_timer = Timer(cooldown / 1000)
        self.shoot_timer.start()

    def fire(self, client_time):
        if not self.shoot_timer.is_time_passed(): return
        self.shoot_timer.start()

        self.broadcast_command_only_to_other_players("shoot", (self.owner_id,))

    def fire_static(self, client_time, hit_point):
        if not self.shoot_timer.is_time_passed(): return
        self.shoot_timer.start()

        self.broadcast_command_only_to_other_players("shoot_static", (self.owner_id, hit_point))

    def fire_target(self, client_time, target_id, target_incarnation, target_pos, hit_point, hit_point_word):
        if not self.shoot_timer.is_time_passed(): return
        self.shoot_timer.start()

        max_damage = self.max_damage
        min_damage = self.max_damage

        is_critical_hit = random.random() < self.critical_hit_chance

        if is_critical_hit:
            max_damage += self.critical_hit_damage
            min_damage += self.critical_hit_damage

        damage, impact_coff = self.weapon_common_global_model.calculate_damage_and_impact_coff(target_pos, min_damage, max_damage)
        self.weapon_common_global_model.apply_damage_to_target(target_id, damage, TURRET_PROTECTION_NAME)

        self.broadcast_command_only_to_other_players("shoot_target", (self.owner_id, target_id, hit_point, impact_coff, is_critical_hit))
