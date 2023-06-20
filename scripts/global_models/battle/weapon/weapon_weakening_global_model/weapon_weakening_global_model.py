from client.layouts.battle.models.weapon_weakening_model import weapon_weakening_model
from space.global_model import GlobalModel
from . import weapon_weakening_model_cc

import math

class WeaponWeakeningGlobalModel(GlobalModel):

    CLIENT_MODEL = weapon_weakening_model.WeaponWeakeningModel

    def __init__(self, global_game_object, global_space, turret_database_item, owner_id=None):
        super().__init__(global_game_object, global_space, owner_id)

        self.weapon_weakening_model_cc = self.create_weapon_weakening_model_cc(turret_database_item)

        self.maximum_damage_radius = self.weapon_weakening_model_cc.maximum_damage_radius
        self.minimum_damage_radius = self.weapon_weakening_model_cc.minimum_damage_radius
        self.minimum_damage_percent = self.weapon_weakening_model_cc.minimum_damage_percent
        self.falloff_interval = self.minimum_damage_radius - self.maximum_damage_radius

    def create_weapon_weakening_model_cc(self, turret_database_item):
        _weapon_weakening_model_cc = weapon_weakening_model_cc.WeaponWeakeningModelCC()
        _weapon_weakening_model_cc.maximum_damage_radius = turret_database_item.get_property_value("weapon_max_damage_radius")
        _weapon_weakening_model_cc.minimum_damage_percent = turret_database_item.get_property_value("weapon_min_damage_percent")
        _weapon_weakening_model_cc.minimum_damage_radius = turret_database_item.get_property_value("weapon_min_damage_radius")
        return _weapon_weakening_model_cc

    def get_model_data(self):
        return self.weapon_weakening_model_cc

    def get_impact_coeff(self, distance):
        if self.falloff_interval <= 0:
            return 1

        if distance <= self.maximum_damage_radius:
            return 1

        if distance >= self.minimum_damage_radius:
            return 0.01 * self.minimum_damage_percent

        return 0.01 * (self.minimum_damage_percent + (self.minimum_damage_radius - distance) * (100 - self.minimum_damage_percent) / self.falloff_interval)

    def calculate_damage(self, distance, min_damage, max_damage):
        damage = self.calculate_range_damage(distance, min_damage, max_damage)
        return self.weaken_damage(damage, distance)

    def calculate_range_damage(self, distance, min_damage, max_damage):
        if distance <= self.maximum_damage_radius:
            return max_damage

        if distance >= self.minimum_damage_radius:
            return min_damage

        multiplier = (distance - self.maximum_damage_radius) / self.minimum_damage_radius
        return min_damage + (max_damage - min_damage) * multiplier

    def weaken_damage(self, damage, distance):
        if distance <= self.maximum_damage_radius:
            return damage

        if self.minimum_damage_percent > 100.0:
            self.minimum_damage_percent = 100.0

        if distance >= self.minimum_damage_radius:
            percent = self.minimum_damage_percent
        else:
            percent = self.minimum_damage_percent + (self.minimum_damage_radius - distance) * (100.0 - self.minimum_damage_percent) / (self.minimum_damage_radius - self.maximum_damage_radius)

        return (math.ceil(percent / 100.0 * damage))
