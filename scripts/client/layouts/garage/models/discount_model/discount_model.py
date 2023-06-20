from client.layouts.garage.models.discount_model import discount_model_data
from client.space.model import Model

class DiscountModel(Model):
    model_id = 300040006

    def __init__(self, game_object, client_space, client_object, garage_item_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.model_data = discount_model_data.DiscountModelData(game_object, client_object, garage_item_object)
        self.commands = None
        self.command_handler = None
