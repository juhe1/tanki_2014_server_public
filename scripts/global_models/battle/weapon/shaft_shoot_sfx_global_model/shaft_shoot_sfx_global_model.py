from client.layouts.battle.models.shaft_shoot_sfx_model import shaft_shoot_sfx_model
from loaders.client_resource_loader import client_resource_loader
from space.global_model import GlobalModel
from . import shaft_shoot_sfx_model_cc

class ShaftShootSfxGlobalModel(GlobalModel):

    CLIENT_MODEL = shaft_shoot_sfx_model.ShaftShootSfxModel

    def __init__(self, global_game_object, global_space, turret_garage_item, owner_id=None):
        super().__init__(global_game_object, global_space, owner_id)

        self.shaft_shoot_sfx_model_cc = self.create_shaft_shoot_sfx_cc(turret_garage_item)

    def create_shaft_shoot_sfx_cc(self, turret_garage_item):
        shaft_sfx_data = turret_garage_item.sfx_data
        _shaft_shoot_sfx_model_cc = shaft_shoot_sfx_model_cc.ShaftShootSfxModelCC()
        _shaft_shoot_sfx_model_cc.explosion_sound = client_resource_loader.get_resource_id(shaft_sfx_data.explosion_sound)
        _shaft_shoot_sfx_model_cc.explosion_texture = client_resource_loader.get_resource_id(shaft_sfx_data.explosion_texture)
        _shaft_shoot_sfx_model_cc.hit_mark_texture = client_resource_loader.get_resource_id(shaft_sfx_data.hit_mark_texture)
        _shaft_shoot_sfx_model_cc.muzzle_flash_texture = client_resource_loader.get_resource_id(shaft_sfx_data.muzzle_flash_texture)
        _shaft_shoot_sfx_model_cc.shot_sound = client_resource_loader.get_resource_id(shaft_sfx_data.shot_sound)
        _shaft_shoot_sfx_model_cc.targeting_sound = client_resource_loader.get_resource_id(shaft_sfx_data.targeting_sound)
        _shaft_shoot_sfx_model_cc.trail_texture = client_resource_loader.get_resource_id(shaft_sfx_data.trail_texture)
        _shaft_shoot_sfx_model_cc.zoom_mode_sound = client_resource_loader.get_resource_id(shaft_sfx_data.zoom_mode_sound)
        return _shaft_shoot_sfx_model_cc

    def get_model_data(self):
        return self.shaft_shoot_sfx_model_cc
