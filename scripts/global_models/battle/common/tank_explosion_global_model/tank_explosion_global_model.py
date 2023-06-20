from client.layouts.battle.models.tank_explosion_model import tank_explosion_model
from loaders.client_resource_loader import client_resource_loader
from space.global_model import GlobalModel
from . import tank_explosion_model_cc

class TankExplosionGlobalModel(GlobalModel):

    CLIENT_MODEL = tank_explosion_model.TankExplosionModel

    def __init__(self, global_game_object, global_space, owner_id=None):
        super().__init__(global_game_object, global_space, owner_id)

        self.tank_explosion_model_cc = self.create_cc()

    def create_cc(self):
        _tank_explosion_model_cc = tank_explosion_model_cc.TankExplosionModelCC()
        _tank_explosion_model_cc.explosion_texture = client_resource_loader.get_resource_id("/battle/multiframe_image/tank_explosion/explosion")
        _tank_explosion_model_cc.shock_wave_texture = client_resource_loader.get_resource_id("/battle/multiframe_image/tank_explosion/shock_wave")
        _tank_explosion_model_cc.smoke_texture = client_resource_loader.get_resource_id("/battle/multiframe_image/tank_explosion/smoke")
        return _tank_explosion_model_cc

    def get_model_data(self):
        return self.tank_explosion_model_cc
