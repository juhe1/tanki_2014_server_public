from client.layouts.garage.models.upgradeable_params_constructor_model import upgradeable_params_constructor_model_data
from client.space.model import Model

class UpgradeableParamsConstructorModel(Model):
    model_id = 300040026

    def __init__(self, game_object, client_space, client_object, garage_item_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)
        
        self.model_data = upgradeable_params_constructor_model_data.UpgradeableParamsConstructorModelData(game_object, client_object, garage_item_object, self)
        self.commands = None
        self.command_handler = None
