from client.layouts.battle.models.stream_weapon_model import stream_weapon_model
from space.global_model import GlobalModel
from . import stream_weapon_model_cc
import time

class StreamWeaponGlobalModel(GlobalModel):

    CLIENT_MODEL = stream_weapon_model.StreamWeaponModel

    def __init__(self, global_game_object, global_space, turret_database_item, weapon_common_global_model, owner_id=None):
        super().__init__(global_game_object, global_space, owner_id)

        self.weapon_common_global_model = weapon_common_global_model
        self.stream_weapon_model_cc = self.create_cc(turret_database_item)

        self.min_damage = turret_database_item.get_property_value("damage_to")
        self.max_damage = turret_database_item.get_property_value("damage_from")

        self.energy = self.stream_weapon_model_cc.energy_capacity
        self.fire_start_time = 0
        self.fire_stop_time = 0
        self.last_tick_time = 0

    # TODO: fill energy affter respawning

    def calculate_energy(self, is_firing):
        if is_firing:
            energy = self.energy - (time.time() - self.fire_start_time) * self.stream_weapon_model_cc.energy_discharge_speed
        else:
            energy = self.energy + (time.time() - self.fire_stop_time) * self.stream_weapon_model_cc.energy_recharge_speed

        energy_clamped = max(0, min(energy, self.stream_weapon_model_cc.energy_capacity))
        return energy_clamped

    def hit(self, _time, targets, incarnations, target_positions, hit_points_world, turret_protection_name):
        if time.time() - self.last_tick_time < self.stream_weapon_model_cc.weapon_tick_interval_msec / 1000: return False
        if self.calculate_energy(True) == 0: return False

        self.last_tick_time = time.time()

        for target_id, target_position in zip(targets, target_positions):
            self.weapon_common_global_model.check_shooting_params(target_id, target_position)
            damage, impact_coff = self.weapon_common_global_model.calculate_damage_and_impact_coff(target_position, self.min_damage, self.max_damage)
            self.weapon_common_global_model.apply_damage_to_target(target_id, damage, turret_protection_name)

        return True

    def start_fire(self):
        self.fire_start_time = time.time()
        self.energy = self.calculate_energy(False)

    def stop_fire(self):
        self.fire_stop_time = time.time()
        self.energy = self.calculate_energy(True)

    def create_cc(self, turret_database_item):
        stream_weapon_data = turret_database_item.garage_item.stream_weapon_data

        cc = stream_weapon_model_cc.StreamWeaponModelCC()
        cc.energy_capacity = stream_weapon_data.energy_capacity
        cc.energy_discharge_speed = turret_database_item.get_property_value("weapon_discharge_rate")
        cc.energy_recharge_speed = cc.energy_capacity / turret_database_item.get_property_value("weapon_reload_time")
        cc.weapon_tick_interval_msec = stream_weapon_data.weapon_tick_interval_msec

        return cc

    def get_model_data(self):
        return self.stream_weapon_model_cc
