from client.layouts.battle.models.freeze_sfx_model import freeze_sfx_model
from space.global_model import GlobalModel
from . import freeze_sfx_model_cc
from loaders.client_resource_loader import client_resource_loader

class FreezeSfxGlobalModel(GlobalModel):

    CLIENT_MODEL = freeze_sfx_model.FreezeSfxModel

    def __init__(self, global_game_object, global_space, sfx_data, owner_id=None):
        super().__init__(global_game_object, global_space, owner_id)

        self.freeze_sfx_model_cc = self.create_cc(sfx_data)

    def create_cc(self, sfx_data):
        cc = freeze_sfx_model_cc.FreezeSfxModelCC()
        cc.particle_speed = sfx_data.particle_speed
        cc.particle_texture = client_resource_loader.get_resource_id(sfx_data.particle_texture)
        cc.plane_texture = client_resource_loader.get_resource_id(sfx_data.plane_texture)
        cc.shot_sound = client_resource_loader.get_resource_id(sfx_data.shot_sound)
        return cc

    def get_model_data(self):
        return self.freeze_sfx_model_cc
