from . import weapon_weakening_model_data
from client.space.model import Model

import math

class WeaponWeakeningModel(Model):
    model_id = 300100094

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.model_data = weapon_weakening_model_data.WeaponWeakeningModelData(game_object, global_model.get_model_data())
        self.commands = None
        self.command_handler = None
