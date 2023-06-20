from global_models.battle_list.common.map_info_global_model import map_info_global_model
from client.layouts.battle.models.battle_map_model import battle_map_model
from loaders.graphics_settings_loader import graphics_settings_loader
from space.global_model import GlobalModel
from loaders.map_loader import map_loader
from space import global_space_registry
from . import battle_map_model_cc

class BattleMapGlobalModel(GlobalModel):

    CLIENT_MODEL = battle_map_model.BattleMapModel

    def __init__(self, global_game_object, global_space, battle_info_global_model, owner_id=None):
        super().__init__(global_game_object, global_space, owner_id)

        self.map_info = self.get_map_info(battle_info_global_model.battle_info_model_cc.map_game_object_id)
        self.battle_map_model_cc = self.create_cc()

    def get_map_info(self, map_game_object_id):
        _map_info_global_model = global_space_registry.get_global_model(map_info_global_model.MapInfoGlobalModel, global_game_object_id=map_game_object_id, global_space_name="battle_select")
        map_id = _map_info_global_model.get_model_data().map_id
        return map_loader.get_map_by_id(map_id)

    def create_cc(self):
        map_info = self.map_info
        map_graphics_settings = graphics_settings_loader.get_graphics_settings_by_name(map_info.graphics_settings)

        _battle_map_model_cc = battle_map_model_cc.BattleMapModelCC()
        _battle_map_model_cc.dust_params = map_graphics_settings.dust_params
        _battle_map_model_cc.dynamic_shadow_params = map_graphics_settings.dynamic_shadow_params
        _battle_map_model_cc.environment_sound_resource_id = map_info.environment_sound
        _battle_map_model_cc.fog_params = map_graphics_settings.fog_params
        _battle_map_model_cc.gravity = map_info.gravity
        _battle_map_model_cc.map_resource_id = map_info.map_resource
        _battle_map_model_cc.sky_box_revolution_axis = map_info.sky_box_revolution_axis
        _battle_map_model_cc.sky_box_revolution_speed = map_info.sky_box_revolution_speed
        _battle_map_model_cc.sky_box_resource_id = map_info.sky_box
        _battle_map_model_cc.ssao_color = map_graphics_settings.ssao_color
        return _battle_map_model_cc

    def get_model_data(self):
        return self.battle_map_model_cc
