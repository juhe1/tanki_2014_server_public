from client.layouts.battle.models.smoky_shoot_sfx_model import smoky_shoot_sfx_model
from loaders.client_resource_loader import client_resource_loader
from space.global_model import GlobalModel
from . import smoky_shoot_sfx_model_cc

class SmokyShootSfxGlobalModel(GlobalModel):

    CLIENT_MODEL = smoky_shoot_sfx_model.SmokyShootSfxModel

    def __init__(self, global_game_object, global_space, turret_garage_item, owner_id=None):
        super().__init__(global_game_object, global_space, owner_id)
        self.smoky_shoot_sfx_model_cc = self.create_smoky_shoot_sfx_cc(turret_garage_item)

    def create_smoky_shoot_sfx_cc(self, turret_garage_item):
        smoky_sfx_data = turret_garage_item.sfx_data
        _smoky_shoot_sfx_model_cc = smoky_shoot_sfx_model_cc.SmokyShootSfxModelCC()
        _smoky_shoot_sfx_model_cc.critical_hit_size = smoky_sfx_data.critical_hit_size
        _smoky_shoot_sfx_model_cc.critical_hit_texture = client_resource_loader.get_resource_id(smoky_sfx_data.critical_hit_texture)
        _smoky_shoot_sfx_model_cc.explosion_mark_texture = client_resource_loader.get_resource_id(smoky_sfx_data.explosion_mark_texture)
        _smoky_shoot_sfx_model_cc.explosion_size = smoky_sfx_data.explosion_size
        _smoky_shoot_sfx_model_cc.explosion_sound = client_resource_loader.get_resource_id(smoky_sfx_data.explosion_sound)
        _smoky_shoot_sfx_model_cc.explosion_texture = client_resource_loader.get_resource_id(smoky_sfx_data.explosion_texture)
        _smoky_shoot_sfx_model_cc.shot_sound = client_resource_loader.get_resource_id(smoky_sfx_data.shot_sound)
        _smoky_shoot_sfx_model_cc.shot_texture = client_resource_loader.get_resource_id(smoky_sfx_data.shot_texture)
        return _smoky_shoot_sfx_model_cc

    def get_model_data(self):
        return self.smoky_shoot_sfx_model_cc
