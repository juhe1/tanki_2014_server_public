from client.layouts.garage.models.description_model import description_model_data
from client.space.model import Model

class DescriptionModel(Model):
    model_id = 170002

    def __init__(self, game_object, client_space, client_object, garage_item_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)
        
        self.model_data = description_model_data.DescriptionModelData(game_object, client_object, garage_item_object)
        self.commands = None
        self.command_handler = None
