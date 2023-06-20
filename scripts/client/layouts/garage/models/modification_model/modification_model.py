from client.layouts.garage.models.modification_model import modification_model_data
from client.space.model import Model

class ModificationModel(Model):
    model_id = 300040016

    def __init__(self, game_object, client_space, client_object, garage_item_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)
        
        self.model_data = modification_model_data.ModificationModelData(game_object, client_object, garage_item_object)
        self.commands = None
        self.command_handler = None
