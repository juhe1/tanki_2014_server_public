from client.layouts.battle.models.flame_throwing_sfx_model import flame_throwing_sfx_model
from space.global_model import GlobalModel
from loaders.client_resource_loader import client_resource_loader
from . import flame_throwing_sfx_model_cc

class FlameThrowingSfxGlobalModel(GlobalModel):

    CLIENT_MODEL = flame_throwing_sfx_model.FlameThrowingSfxModel

    def __init__(self, global_game_object, global_space, turret_garage_item, owner_id=None):
        super().__init__(global_game_object, global_space, owner_id)

        self.flame_throwing_sfx_model_cc = self.create_cc(turret_garage_item)

    def create_cc(self, turret_garage_item):
        flame_thrower_sfx_data = turret_garage_item.sfx_data
        _flame_throwing_sfx_model_cc = flame_throwing_sfx_model_cc.FlameThrowingSfxModelCC()
        _flame_throwing_sfx_model_cc.fire_texture = client_resource_loader.get_resource_id(flame_thrower_sfx_data.fire_texture)
        _flame_throwing_sfx_model_cc.flame_sound = client_resource_loader.get_resource_id(flame_thrower_sfx_data.flame_sound)
        _flame_throwing_sfx_model_cc.muzzle_plane_texture = client_resource_loader.get_resource_id(flame_thrower_sfx_data.muzzle_plane_texture)
        return _flame_throwing_sfx_model_cc

    def get_model_data(self):
        return self.flame_throwing_sfx_model_cc
