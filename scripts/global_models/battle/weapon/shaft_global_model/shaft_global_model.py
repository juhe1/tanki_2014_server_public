from client.layouts.battle.models.shaft_model import shaft_model
from loaders.client_resource_loader import client_resource_loader
from global_models.battle.common.bcsh_global_model import bcsh_global_model
from global_models.battle.weapon.shaft_shoot_sfx_global_model import shaft_shoot_sfx_global_model
from global_models.battle.weapon.weapon_common_global_model import weapon_common_global_model
from space.global_model import GlobalModel
from . import shaft_model_cc

import time

TURRET_PROTECTION_NAME = "shaft_resistance"
IMPACT_FORCE_FACTOR = 5000000

class ShaftGlobalModel(GlobalModel):

    CLIENT_MODEL = shaft_model.ShaftModel

    def __init__(self, global_game_object, global_space, turret_database_item, owner_id=None):
        super().__init__(global_game_object, global_space, owner_id)

        self.turret_database_item = turret_database_item
        self.weapon_common_global_model = global_game_object.get_global_model(weapon_common_global_model.WeaponCommonGlobalModel)
        self.shaft_model_cc = self.create_cc()

        self.create_models()

        self.scope_max_damage = self.turret_database_item.get_property_value("shaft_aiming_mode_max_damage")
        self.scope_min_damage = self.turret_database_item.get_property_value("shaft_aiming_mode_min_damage")
        self.max_damage = self.turret_database_item.get_property_value("damage_from")
        self.min_damage = self.turret_database_item.get_property_value("damage_to")
        self.impact_force = self.turret_database_item.get_property_value("impact_force")
        
        self.manual_targeting_activated = False
        self.drain_started_time = None
        self.last_energy_check = time.time() - 100
        self.energy = self.shaft_model_cc.max_energy

    def create_models(self):
        self.global_game_object.add_global_model(shaft_shoot_sfx_global_model.ShaftShootSfxGlobalModel, model_args=(self.turret_database_item.garage_item,))
        self.global_game_object.add_global_model(bcsh_global_model.BcshGlobalModel, model_args=(self.turret_database_item.garage_item.bcsh_data,))

    def activate_manual_targeting(self):
        if not self.has_enought_energy(): return
        self.energy = 0
        self.manual_targeting_activated = True
        self.broadcast_command_only_to_other_players("activate_manual_targeting", (self.owner_id,))

    def stop_manual_targeting(self):
        self.manual_targeting_activated = False
        self.energy = 0
        self.last_energy_check = time.time()
        self.broadcast_command_only_to_other_players("stop_manual_targeting", (self.owner_id,))

    def begin_energy_drain(self):
        self.drain_started_time = time.time()

    def has_enought_energy(self):
        self.energy += (time.time() - self.last_energy_check) * self.shaft_model_cc.charge_rate
        self.last_energy_check = time.time() 

        if self.energy < self.shaft_model_cc.max_energy:
            return False
        
        self.energy = self.shaft_model_cc.max_energy
        return True

    def sort_positions_and_ids_by_distance(self, positions, ids, origin_pos):
        positions_and_ids = [(a, b) for a, b in zip(positions, ids)]

        # short by length, so make the closest opponent to be first in list etc
        sorted_target_positions_and_ids = sorted(positions_and_ids, key=lambda pos: (pos[0] - origin_pos).length())
        return sorted_target_positions_and_ids

    def calculate_drainend_energy(self):
        drained_energy = (time.time() - self.drain_started_time) * self.shaft_model_cc.discharge_rate
        return self.shaft_model_cc.max_energy if drained_energy > self.shaft_model_cc.max_energy else drained_energy

    def calculate_aimed_shot_damage(self):
        energy_drained_factor = self.calculate_drainend_energy() / self.shaft_model_cc.max_energy
        return self.scope_min_damage + (self.scope_max_damage - self.scope_min_damage) * energy_drained_factor

    def aimed_shot(self, _time, static_hit_point, target_ids, target_hit_points, target_incarnations, target_positions, hit_points):
        if not self.manual_targeting_activated: return

        no_scope_impact_force = self.impact_force * IMPACT_FORCE_FACTOR
        aiming_impact = self.shaft_model_cc.aiming_impact * IMPACT_FORCE_FACTOR
        impact_force = no_scope_impact_force + (aiming_impact - no_scope_impact_force) * self.calculate_drainend_energy() / self.shaft_model_cc.max_energy

        self.broadcast_command_only_to_other_players("fire", (self.owner_id, static_hit_point, target_ids, target_hit_points, impact_force))
        self.broadcast_command_only_to_other_players("stop_manual_targeting", (self.owner_id,))

        if target_ids == None:
            return

        damage = self.calculate_aimed_shot_damage()

        own_position = self.weapon_common_global_model.tank_global_model.tank_state.position
        sorted_target_positions_and_ids = self.sort_positions_and_ids_by_distance(target_positions, target_ids, own_position)

        for target_position, target_id in sorted_target_positions_and_ids:
            if self.weapon_common_global_model.check_shooting_params(target_id, target_position) == False:
                continue

            self.weapon_common_global_model.apply_damage_to_target(target_id, damage, TURRET_PROTECTION_NAME)
            damage = damage * self.shaft_model_cc.weakening_coeff

    def quick_shot(self, _time, static_hit_point, target_ids, target_hit_points, target_incarnations, target_positions, hit_points):
        if not self.has_enought_energy(): return

        self.energy -= self.shaft_model_cc.fast_shot_energy
        self.energy = 0 if self.energy < 0 else self.energy

        self.broadcast_command_only_to_other_players("fire", (self.owner_id, static_hit_point, target_ids, target_hit_points, self.impact_force * IMPACT_FORCE_FACTOR))

        if target_ids == None:
            return

        own_position = self.weapon_common_global_model.tank_global_model.tank_state.position
        sorted_target_positions_and_ids = self.sort_positions_and_ids_by_distance(target_positions, target_ids, own_position)

        for target_position, target_id in sorted_target_positions_and_ids:
            if self.weapon_common_global_model.check_shooting_params(target_id, target_position) == False: continue
            result = self.weapon_common_global_model.calculate_damage_and_impact_coff(target_position, self.min_damage, self.max_damage)
            if result is None: return

            damage, impact_coff = result
            self.weapon_common_global_model.apply_damage_to_target(target_id, damage, TURRET_PROTECTION_NAME)
        
    def create_cc(self):
        weapon_data = self.turret_database_item.garage_item.weapon_data
        cc = shaft_model_cc.ShaftModelCC()
        cc.after_shot_pause = weapon_data.after_shot_pause
        cc.aiming_impact = self.turret_database_item.get_property_value("shaft_aimed_shot_impact")
        cc.max_energy = weapon_data.max_energy
        cc.discharge_rate = self.turret_database_item.get_property_value("shaft_aiming_mode_charge_rate")
        cc.charge_rate = cc.max_energy / (self.turret_database_item.get_property_value("weapon_reload_time") / 1000)
        cc.fast_shot_energy = weapon_data.fast_shot_energy
        cc.horizontal_targeting_speed = self.turret_database_item.get_property_value("shaft_horizontal_targeting_speed")
        cc.initial_fov = weapon_data.initial_fov
        cc.jitter_angle_max = weapon_data.jitter_angle_max
        cc.jitter_angle_min = weapon_data.jitter_angle_min
        cc.jitter_intencity_max = weapon_data.jitter_intencity_max
        cc.jitter_intencity_min = weapon_data.jitter_intencity_min
        cc.jitter_start_point = weapon_data.jitter_start_point
        cc.minimum_fov = weapon_data.minimum_fov
        cc.reticle_image = client_resource_loader.get_resource_id(weapon_data.reticle_image)
        cc.rotation_coeff_kmin = 1
        cc.rotation_coeff_T1 = 1
        cc.rotation_coeff_T2 = 1
        cc.shrubs_hiding_radius_max = weapon_data.shrubs_hiding_radius_max
        cc.shrubs_hiding_radius_min = weapon_data.shrubs_hiding_radius_min
        cc.targeting_acceleration = weapon_data.targeting_acceleration
        cc.targeting_transition_time = weapon_data.targeting_transition_time
        cc.vertical_targeting_speed = self.turret_database_item.get_property_value("shaft_vertical_targeting_speed")
        cc.weakening_coeff = weapon_data.weakening_coeff
        return cc

    def get_model_data(self):
        return self.shaft_model_cc
