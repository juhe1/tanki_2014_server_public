from client.layouts.battle.models.weapon_common_model import weapon_common_model
from global_models.battle.weapon.discrete_shot_global_model import discrete_shot_global_model
from global_models.battle.common.lighting_sfx_global_model import lighting_sfx_global_model
from global_models.battle.common.object_3ds_global_model import object_3ds_global_model
from global_models.battle.weapon.flame_thrower_global_model import flame_thrower_global_model
from global_models.battle.weapon.freeze_global_model import freeze_global_model
from global_models.battle.weapon.stream_weapon_global_model import stream_weapon_global_model
from global_models.battle.weapon.smoky_global_model import smoky_global_model
from global_models.battle.weapon.shaft_global_model import shaft_global_model
from global_models.battle.common.tank_global_model.tank_state import LogicStateEnum
from global_models.battle.common.tank_global_model import tank_global_model
from global_models.battle.weapon.weapon_weakening_global_model import weapon_weakening_global_model
from space.global_model import GlobalModel
from . import weapon_common_model_cc
import server_properties

class WeaponCommonGlobalModel(GlobalModel):

    CLIENT_MODEL = weapon_common_model.WeaponCommonModel

    def __init__(self, global_game_object, global_space, turret_database_item, owner_id=None):
        super().__init__(global_game_object, global_space, owner_id)

        self.turret_database_item = turret_database_item
        self.turret_garage_item = turret_database_item.garage_item

        self.weapon_common_model_cc = self.create_weapon_common_model_cc()
        self.tank_global_model = None

    def init(self, _tank_global_model):
        self.tank_global_model = _tank_global_model
        self.add_global_models()
        self.weapon_weakening_global_model = self.global_game_object.get_global_model(weapon_weakening_global_model.WeaponWeakeningGlobalModel)

    def check_shooting_params(self, target_id, target_pos):
        target_tank_global_model = self.global_space.get_global_model(tank_global_model.TankGlobalModel, global_game_object_id=target_id)
        if target_tank_global_model == None: return

        # return, if taget tank or own tank is not active
        if not target_tank_global_model.logic_state.state == LogicStateEnum.ACTIVE or not self.tank_global_model.logic_state.state == LogicStateEnum.ACTIVE:
            return False

        target_real_position = target_tank_global_model.tank_state.position

        # return, if target real position and the position that we get from client is too different
        if (target_real_position - target_pos).length() > server_properties.MAXIMUM_ALLOWED_TANK_POSITION_DIFFERENCE:
            return False

        return True

    def calculate_impact_coff(self, target_pos):
        own_position = self.tank_global_model.tank_state.position
        target_distance = (target_pos - own_position).length() # we are using position that we got from client, because server position is not 100% accurate
        return self.weapon_weakening_global_model.get_impact_coeff(target_distance)

    def calculate_damage_and_impact_coff(self, target_pos, min_damage, max_damage):
        own_position = self.tank_global_model.tank_state.position
        target_distance = (target_pos - own_position).length() # we are using position that we got from client, because server position is not 100% accurate
        impact_coff = self.weapon_weakening_global_model.get_impact_coeff(target_distance)

        damage = self.weapon_weakening_global_model.calculate_damage(target_distance, min_damage, max_damage)
        return damage, impact_coff

    def apply_damage_to_target(self, target_id, damage, turret_protection_name):
        target_tank_global_model = self.global_space.get_global_model(tank_global_model.TankGlobalModel, global_game_object_id=target_id)
        if target_tank_global_model == None: return

        target_tank_global_model.damage_tank(damage, self.tank_global_model, turret_protection_name)

    def add_global_models(self):
        def create_discrete_shot_global_model():
            self.global_game_object.add_global_model(discrete_shot_global_model.DiscreteShotGlobalModel, model_args=(self.turret_database_item,))

        def create_stream_weapon_global_model():
            self.global_game_object.add_global_model(stream_weapon_global_model.StreamWeaponGlobalModel, model_args=(self.turret_database_item, self))

        self.global_game_object.add_global_model(object_3ds_global_model.Object3DSGlobalModel, model_args=(self.turret_garage_item.object_3ds,))
        self.global_game_object.add_global_model(weapon_weakening_global_model.WeaponWeakeningGlobalModel, model_args=(self.turret_database_item,))
        self.global_game_object.add_global_model(lighting_sfx_global_model.LightingSfxGlobalModel, model_args=(self.turret_garage_item.lighting_effects,))

        if self.turret_garage_item.name == "Smoky":
            create_discrete_shot_global_model()
            self.global_game_object.add_global_model(smoky_global_model.SmokyGlobalModel, model_args=(self.turret_database_item,), owner_id=self.owner_id)

        if self.turret_garage_item.name == "Shaft":
            create_discrete_shot_global_model()
            self.global_game_object.add_global_model(shaft_global_model.ShaftGlobalModel, model_args=(self.turret_database_item,), owner_id=self.owner_id)

        if self.turret_garage_item.name == "Firebird":
            create_stream_weapon_global_model()
            self.global_game_object.add_global_model(flame_thrower_global_model.FlameThrowerGlobalModel, model_args=(self.turret_database_item, self.tank_global_model), owner_id=self.owner_id)

        if self.turret_garage_item.name == "Freeze":
            create_stream_weapon_global_model()
            self.global_game_object.add_global_model(freeze_global_model.FreezeGlobalModel, model_args=(self.turret_database_item, self.tank_global_model), owner_id=self.owner_id)

    def create_weapon_common_model_cc(self):
        _weapon_common_model_cc = weapon_common_model_cc.WeaponCommonModelCC()
        _weapon_common_model_cc.impact_force = self.turret_database_item.get_property_value("impact_force")
        _weapon_common_model_cc.kickback = self.turret_database_item.get_property_value("weapon_kickback")
        _weapon_common_model_cc.turret_rotation_acceleration = self.turret_database_item.get_property_value("turret_rotation_acceleration")
        _weapon_common_model_cc.turret_rotation_speed = self.turret_database_item.get_property_value("turret_turn_speed")
        return _weapon_common_model_cc

    def get_model_data(self):
        return self.weapon_common_model_cc
