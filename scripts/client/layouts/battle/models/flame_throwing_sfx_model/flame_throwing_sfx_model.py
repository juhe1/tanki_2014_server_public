from . import flame_throwing_sfx_model_data
from client.space.model import Model

class FlameThrowingSfxModel(Model):
    model_id = 300100045

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.model_data = flame_throwing_sfx_model_data.FlameThrowingSfxModelData(global_model.get_model_data())
