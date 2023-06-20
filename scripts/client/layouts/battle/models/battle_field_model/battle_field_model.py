from global_models.battle.common.tank_rank_up_effect_global_model import tank_rank_up_effect_global_model
from global_models.battle.bonus.battle_field_bonus_global_model import battle_field_bonus_global_model
from global_models.battle.weapon.weapon_common_global_model import weapon_common_global_model
from client.layouts.lobby.models.lobby_layout_notify_model import lobby_layout_notify_model
from global_models.battle.common.lighting_sfx_global_model import lighting_sfx_global_model
from global_models.battle.common.tank_explosion_global_model import tank_explosion_global_model
from global_models.battle.common.object_3ds_global_model import object_3ds_global_model
from client.layouts.battle.tank.tank_initialization_data import TankInitializationData
from global_models.battle.common.tank_global_model.tank_model_cc import TankModelCC
from global_models.battle.common.coloring_global_model import coloring_global_model
from global_models.battle.common.tank_global_model import tank_global_model
from client.layouts.battle.models.inventory_model import inventory_model
from loaders.client_resource_loader import client_resource_loader
from client.layouts.battle.tank.tank_parts import TankParts
from . import battle_field_model_command_handler
from . import battle_field_model_commands
from . import battle_field_model_data
from client.space.model import Model

class BattleFieldModel(Model):
    model_id = 300100008

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        client_object.resource_loader.load_resource("battle\\", language=self.client_object.language)

        self.model_data = battle_field_model_data.BattleFieldModelData(game_object, client_object, global_model)
        self.commands = battle_field_model_commands.BattleFieldModelCommands(self.client_space, game_object)
        self.command_handler = battle_field_model_command_handler.BattleFieldModelCommandHandler()

        self.battle_field_global_space = self.global_model.global_space

        self.tank_database_item = None
        self.tank_garage_item = None
        self.turret_database_item = None
        self.turret_garage_item = None
        self.color_database_item = None
        self.color_garage_item = None

    def init_done(self):
        if not self.global_model.is_user_spectator(self.client_object.user_id):

            if not self.global_model.battle_info_global_model_data.without_supplies:
                self.game_object.add_model(inventory_model.InventoryModel)

            self.get_mounted_items()
            self.create_tank_global_game_object()

        self.load_game_objects()
        self.end_layout_switch()

    def update_battle_field_global_space(self):
        self.client_object.client_space_registry.update_global_space(self.battle_field_global_space)
        self.client_space.load_unloaded_game_objects_from_client()

    def end_layout_switch(self):
        client_space_registry = self.client_object.client_space_registry
        self.lobby_layout_notify_model = client_space_registry.get_model(space_name="lobby", game_object_name="default_game_object", model=lobby_layout_notify_model.LobbyLayoutNotifyModel)
        self.lobby_layout_notify_model.end_layout_switch()

    def load_bonus_game_objects(self):
        _battle_field_bonus_global_model = self.global_model.global_game_object.get_global_model(battle_field_bonus_global_model.BattleFieldBonusGlobalModel)
        bonus_common_global_models = _battle_field_bonus_global_model.bonus_common_global_model_by_bonus_type.values()
        for bonus_common_global_model in bonus_common_global_models:
            self.client_space.get_game_object_by_id(bonus_common_global_model.global_game_object.id).load_object_from_client()

    def load_game_objects(self):
        self.client_object.client_space_registry.update_global_space(self.battle_field_global_space)
        self.client_space.get_game_object_by_name("battle_map").load_object_from_client()
        self.load_bonus_game_objects()
        self.client_space.load_unloaded_game_objects_from_client()
        self.global_model.update_battle_field_global_space()

    def get_mounted_items(self):
        mounted_items = self.client_object.database_garage_item_loader.get_mounted_items()

        tank_item_id = mounted_items["armor"]
        self.tank_database_item = self.client_object.database_garage_item_loader.get_item_by_id(tank_item_id)
        self.tank_garage_item = self.tank_database_item.garage_item

        turret_item_id = mounted_items["weapon"]
        self.turret_database_item = self.client_object.database_garage_item_loader.get_item_by_id(turret_item_id)
        self.turret_garage_item = self.turret_database_item.garage_item

        color_item_id = mounted_items["color"]
        self.color_database_item = self.client_object.database_garage_item_loader.get_item_by_id(color_item_id)
        self.color_garage_item = self.color_database_item.garage_item

    def create_tank_initialization_data(self):
        tank_initialization_data = TankInitializationData()
        tank_initialization_data.acceleration = self.tank_database_item.get_property_value("hull_acceleration")
        tank_initialization_data.reverse_acceleration = self.tank_garage_item.tank_physics.hull_reverse_acceleration
        tank_initialization_data.reverse_turn_acceleration = self.tank_garage_item.tank_physics.hull_reverse_turn_acceleration
        tank_initialization_data.side_acceleration = self.tank_garage_item.tank_physics.hull_side_acceleration
        tank_initialization_data.speed = self.tank_database_item.get_property_value("hull_speed")
        tank_initialization_data.turn_acceleration = self.tank_garage_item.tank_physics.hull_turn_acceleration
        tank_initialization_data.turn_speed = self.tank_database_item.get_property_value("hull_turn_speed")
        tank_initialization_data.turret_rotation_speed = self.turret_database_item.get_property_value("turret_turn_speed")
        return tank_initialization_data

    def create_color_global_game_object(self):
        color_global_game_object = self.battle_field_global_space.add_global_game_object("color")
        color_global_game_object.add_global_model(coloring_global_model.ColoringGlobalModel, model_args=(self.color_garage_item.coloring,))
        return color_global_game_object

    def create_hull_global_game_object(self):
        hull_global_game_object = self.battle_field_global_space.add_global_game_object("hull")
        hull_global_game_object.add_global_model(object_3ds_global_model.Object3DSGlobalModel, model_args=(self.tank_garage_item.object_3ds,))
        hull_global_game_object.add_global_model(tank_rank_up_effect_global_model.TankRankUpEffectGlobalModel)
        hull_global_game_object.add_global_model(tank_explosion_global_model.TankExplosionGlobalModel)
        return hull_global_game_object

    def create_turret_global_game_object(self):
        turret_global_game_object = self.battle_field_global_space.add_global_game_object("turret")
        turret_global_game_object.add_global_model(weapon_common_global_model.WeaponCommonGlobalModel, model_args=(self.turret_database_item,), owner_id=self.client_object.user_id)
        return turret_global_game_object

    def create_tank_parts(self):
        new_tank_parts = TankParts()
        new_tank_parts.color_id = self.create_color_global_game_object().id
        new_tank_parts.hull_id = self.create_hull_global_game_object().id
        new_tank_parts.weapon_id = self.create_turret_global_game_object().id
        return new_tank_parts

    def create_tank_cc(self):
        tank_model_cc = TankModelCC()
        tank_model_cc.damping = self.tank_garage_item.tank_physics.hull_damping
        tank_model_cc.mass = self.tank_database_item.get_property_value("hull_mass")
        tank_model_cc.max_health = round(self.tank_database_item.get_property_value("hull_armor"))
        tank_model_cc.tank_initialization_data = self.create_tank_initialization_data()
        tank_model_cc.tank_parts = self.create_tank_parts()
        return tank_model_cc

    def create_tank_global_game_object(self):
        tank_model_cc = self.create_tank_cc()
        tank_id = self.client_object.user_id

        tank_global_game_object = self.battle_field_global_space.add_global_game_object("tank_" + str(tank_id), id=tank_id)
        tank_global_game_object.add_global_model(tank_global_model.TankGlobalModel, model_args=(tank_model_cc, self.color_database_item, self.tank_database_item), owner_id=tank_id)
        tank_global_game_object.add_global_model(lighting_sfx_global_model.LightingSfxGlobalModel, model_args=([],)) # TODO: create tank lighting_effects
        return tank_global_game_object
