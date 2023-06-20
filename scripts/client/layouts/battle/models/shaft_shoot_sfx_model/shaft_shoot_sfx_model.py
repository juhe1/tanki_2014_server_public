from . import shaft_shoot_sfx_model_data
from client.space.model import Model

class ShaftShootSfxModel(Model):
    model_id = 300100067

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.model_data = shaft_shoot_sfx_model_data.ShaftShootSfxModelData(global_model.get_model_data())
