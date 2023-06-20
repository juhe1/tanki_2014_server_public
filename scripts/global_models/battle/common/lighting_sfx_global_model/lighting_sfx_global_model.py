from client.layouts.battle.models.lighting_sfx_model import lighting_sfx_model
from space.global_model import GlobalModel
from . import lighting_sfx_model_cc

class LightingSfxGlobalModel(GlobalModel):

    CLIENT_MODEL = lighting_sfx_model.LightingSfxModel

    def __init__(self, global_game_object, global_space, lighting_effects, owner_id=None):
        super().__init__(global_game_object, global_space, owner_id)

        self.lighting_sfx_model_cc = lighting_sfx_model_cc.LightingSfxModelCC()
        self.lighting_sfx_model_cc.lighting_effects = lighting_effects

    def get_model_data(self):
        return self.lighting_sfx_model_cc
