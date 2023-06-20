from client.layouts.battle.models.weapon_weakening_model import weapon_weakening_model
from client.space.model import Model

from . import smoky_model_command_handler
from . import smoky_model_commands

class SmokyModel(Model):
    model_id = 300100070

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.model_data = None
        self.commands = smoky_model_commands.SmokyModelCommands(self.client_space, game_object)

        if global_model.is_owner(client_object.user_id):
            self.command_handler = smoky_model_command_handler.SmokyModelCommandHandler(global_model)
