from client.layouts.garage.models.data_owner_model import data_owner_model_data
from client.space.model import Model

class DataOwnerModel(Model):
    model_id = 300070005

    def __init__(self, game_object, client_space, client_object, data_owner_id, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.model_data = data_owner_model_data.DataOwnerModelData(game_object, data_owner_id)
        self.commands = None
        self.command_handler = None
