from client.layouts.garage.models.temporary_item_model import temporary_item_model_data
from client.space.model import Model

class TemporaryItemModel(Model):
    model_id = 300040019

    def __init__(self, game_object, client_space, client_object, garage_item_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)
        
        self.model_data = temporary_item_model_data.TemporaryItemModelData(game_object, client_object, garage_item_object)
        self.commands = None
        self.command_handler = None
