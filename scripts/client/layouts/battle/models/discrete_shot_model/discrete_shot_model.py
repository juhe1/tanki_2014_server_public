from . import discrete_shot_model_data
from client.space.model import Model

class DiscreteShotModel(Model):
    model_id = 300100032

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.model_data = discrete_shot_model_data.DiscreteShotModelData(game_object, global_model.get_model_data())
        self.commands = None
        self.command_handler = None
