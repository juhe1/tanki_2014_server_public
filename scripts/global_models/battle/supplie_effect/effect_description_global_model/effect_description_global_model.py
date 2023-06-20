from client.layouts.battle.models.effect_description_model import effect_description_model
from space.global_model import GlobalModel
from . import effect_description_model_cc

class EffectDescriptionGlobalModel(GlobalModel):

    CLIENT_MODEL = effect_description_model.EffectDescriptionModel

    def __init__(self, global_game_object, global_space, index, inventory, tank_game_object_id, owner_id=None):
        super().__init__(global_game_object, global_space, owner_id)
        self.effect_description_model_cc = effect_description_model_cc.EffectDescriptionModelCC(index, inventory, tank_game_object_id)

    def get_model_data(self):
        return self.effect_description_model_cc
