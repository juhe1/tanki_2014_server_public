from global_models.battle.weapon.flame_throwing_sfx_global_model import flame_throwing_sfx_global_model 
from global_models.battle.common.tank_global_model import tank_global_model
from global_models.battle.weapon.stream_weapon_global_model import stream_weapon_global_model 
from global_models.battle.common.color_transform_global_model import color_transform_global_model 
from client.layouts.battle.models.flame_thrower_model import flame_thrower_model
from space.global_model import GlobalModel
from . import flame_thrower_model_cc

TURRET_PROTECTION_NAME = "firebird_resistance"

class FlameThrowerGlobalModel(GlobalModel):

    CLIENT_MODEL = flame_thrower_model.FlameThrowerModel

    def __init__(self, global_game_object, global_space, turret_database_item, tank_global_model, owner_id=None):
        super().__init__(global_game_object, global_space, owner_id)

        self.tank_global_model = tank_global_model
        self.turret_database_item = turret_database_item
        self.flame_thrower_data = turret_database_item.garage_item.weapon_data
        self.flame_thrower_model_cc = self.create_cc()
        self.stream_weapon_global_model = global_game_object.get_global_model(stream_weapon_global_model.StreamWeaponGlobalModel)
        self.temperature_limit = self.turret_database_item.get_property_value("flame_temperature_limit")

        self.create_models()

    def create_models(self):
        self.global_game_object.add_global_model(flame_throwing_sfx_global_model.FlameThrowingSfxGlobalModel, model_args=(self.turret_database_item.garage_item,))
        self.global_game_object.add_global_model(color_transform_global_model.ColorTransformGlobalModel, model_args=(self.turret_database_item.garage_item.color_transform_structs,))

    def create_temperature_change_task(self):
        temperature = self.tank_global_model.temperature

        temperature_change_task = temperature.create_temperature_change_task(
            self.flame_thrower_data.cooling_rate, 
            self.temperature_limit,
            self.flame_thrower_data.burn_damage_min,
            self.flame_thrower_data.burn_damage_max,
            0,
            0,
            TURRET_PROTECTION_NAME
        )

        return temperature_change_task

    def hit(self, time, targets, incarnations, target_positions, hit_points_world):
        if self.stream_weapon_global_model.hit(time, targets, incarnations, target_positions, hit_points_world, TURRET_PROTECTION_NAME) == False:
            return

        for target_id in targets:
            target_tank_global_model = self.global_space.get_global_model(tank_global_model.TankGlobalModel, global_game_object_id=target_id)
            target_tank_global_model.temperature.add_temperature(self.flame_thrower_data.heating_rate, self.owner_id, self.create_temperature_change_task)

    def start_fire(self, time):
        self.stream_weapon_global_model.start_fire()
        self.broadcast_command_only_to_other_players("start_fire", (self.owner_id,))

    def stop_fire(self, time):
        self.stream_weapon_global_model.stop_fire()
        self.broadcast_command_only_to_other_players("stop_fire", (self.owner_id,))

    def create_cc(self):
        cc = flame_thrower_model_cc.FlameThrowerModelCC()
        cc.cone_angle = self.turret_database_item.garage_item.weapon_data.cone_angle
        cc.range = self.turret_database_item.get_property_value("weapon_min_damage_radius")
        return cc

    def get_model_data(self):
        return self.flame_thrower_model_cc
