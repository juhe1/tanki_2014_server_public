from . import freeze_sfx_model_data
from client.space.model import Model

class FreezeSfxModel(Model):
    model_id = 300100047

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.model_data = freeze_sfx_model_data.FreezeSfxModelData(global_model.get_model_data())
