from . import tank_explosion_model_data
from client.space.model import Model

class TankExplosionModel(Model):
    model_id = 300100077

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.model_data = tank_explosion_model_data.TankExplosionModelData(game_object, global_model.get_model_data())
        self.commands = None
        self.command_handler = None
