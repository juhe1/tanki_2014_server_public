from client.layouts.garage.models.garage_kit_model import garage_kit_model_data
from client.space.model import Model

class GarageKitModel(Model):
    model_id = 300040007

    def __init__(self, game_object, client_space, client_object, garage_item_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.model_data = garage_kit_model_data.GarageKitModelData(game_object, client_object, garage_item_object)
        self.commands = None
        self.command_handler = None
