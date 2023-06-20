from . import stream_weapon_model_data
from client.space.model import Model

class StreamWeaponModel(Model):
    model_id = 300100075

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.model_data = stream_weapon_model_data.StreamWeaponModelData(global_model.get_model_data())
