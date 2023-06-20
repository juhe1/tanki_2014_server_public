from client.layouts.garage.models.item_category_model import item_category_model_data
from client.space.model import Model

class ItemCategoryModel(Model):
    model_id = 300040010

    def __init__(self, game_object, client_space, client_object, garage_item_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)
        
        self.model_data = item_category_model_data.ItemCategoryModelData(game_object, client_object, garage_item_object)
        self.commands = None
        self.command_handler = None
