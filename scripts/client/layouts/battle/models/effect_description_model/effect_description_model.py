from . import effect_description_model_data
from client.space.model import Model

class EffectDescriptionModel(Model):
    model_id = 300100037

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.model_data = effect_description_model_data.EffectDescriptionModelData(global_model.get_model_data())
