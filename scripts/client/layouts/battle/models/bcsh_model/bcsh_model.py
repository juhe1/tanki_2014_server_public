from client.layouts.battle.models.bcsh_model import bcsh_model_data
from client.space.model import Model

class BcshModel(Model):
    model_id = 300100002

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.model_data = bcsh_model_data.BcshModelData(game_object, global_model.get_model_data())
        self.commands = None
        self.command_handler = None
