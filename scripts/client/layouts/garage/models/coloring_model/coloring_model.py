from client.layouts.garage.models.coloring_model import coloring_model_data
from client.space.model import Model

class ColoringModel(Model):
    model_id = 300070004

    def __init__(self, game_object, client_space, client_object, color_resource_name=None, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)
        
        self.model_data = coloring_model_data.ColoringModelData(game_object, color_resource_name)
        self.commands = None
        self.command_handler = None
