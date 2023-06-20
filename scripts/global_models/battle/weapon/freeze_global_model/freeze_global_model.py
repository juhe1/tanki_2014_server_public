from global_models.battle.weapon.freeze_sfx_global_model import freeze_sfx_global_model
from global_models.battle.common.tank_global_model import tank_global_model
from client.layouts.battle.models.freeze_model import freeze_model
from space.global_model import GlobalModel
from . import freeze_model_cc
from global_models.battle.weapon.stream_weapon_global_model import stream_weapon_global_model 

TURRET_PROTECTION_NAME = "freeze_resistance"

class FreezeGlobalModel(GlobalModel):

    CLIENT_MODEL = freeze_model.FreezeModel

    def __init__(self, global_game_object, global_space, turret_database_item, tank_global_model, owner_id=None):
        super().__init__(global_game_object, global_space, owner_id)

        self.tank_global_model = tank_global_model
        self.turret_database_item = turret_database_item
        self.freeze_data = turret_database_item.garage_item.weapon_data
        self.freeze_model_cc = self.create_cc()
        self.stream_weapon_global_model = global_game_object.get_global_model(stream_weapon_global_model.StreamWeaponGlobalModel)

        self.create_models()

    def create_models(self):
        self.global_game_object.add_global_model(freeze_sfx_global_model.FreezeSfxGlobalModel, model_args=(self.turret_database_item.garage_item.sfx_data,))

    def create_temperature_change_task(self):
        temperature = self.tank_global_model.temperature
        temperature_change_task = temperature.create_temperature_change_task(-self.freeze_data.defrosting_speed, self.freeze_data.min_temperature, 0, 0, self.freeze_data.turret_max_freezing, self.freeze_data.body_max_freezing, TURRET_PROTECTION_NAME)
        return temperature_change_task

    def hit(self, time, targets, incarnations, target_positions, hit_points_world):
        hit_success = self.stream_weapon_global_model.hit(time, targets, incarnations, target_positions, hit_points_world, TURRET_PROTECTION_NAME)
        if not hit_success: return

        for target_id in targets:
            target_tank_global_model = self.global_space.get_global_model(tank_global_model.TankGlobalModel, global_game_object_id=target_id)
            target_tank_global_model.temperature.add_temperature(-self.freeze_data.freezing_speed, self.owner_id, self.create_temperature_change_task)

    def start_fire(self, time):
        self.stream_weapon_global_model.start_fire()
        self.broadcast_command_only_to_other_players("start_fire", (self.owner_id,))

    def stop_fire(self, time):
        self.stream_weapon_global_model.stop_fire()
        self.broadcast_command_only_to_other_players("stop_fire", (self.owner_id,))

    def create_cc(self):
        _freeze_model_cc = freeze_model_cc.FreezeModelCC()
        _freeze_model_cc.cone_angle = self.freeze_data.cone_angle
        _freeze_model_cc.range = self.turret_database_item.get_property_value("weapon_min_damage_radius")
        return _freeze_model_cc

    def get_model_data(self):
        return self.freeze_model_cc
