from . import isis_sfx_model_data
from client.space.model import Model

class IsisSfxModel(Model):
    model_id = 999999999999999

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.model_data = isis_sfx_model_data.IsisSfxModelData(global_model.get_model_data())
