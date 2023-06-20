from client.layouts.battle.models.weapon_common_model import weapon_common_model_data
from client.space.model import Model

class WeaponCommonModel(Model):
    model_id = 300100093

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)
        self.model_data = weapon_common_model_data.WeaponCommonModelData(game_object, global_model.get_model_data())
        self.commands = None
        self.command_handler = None
