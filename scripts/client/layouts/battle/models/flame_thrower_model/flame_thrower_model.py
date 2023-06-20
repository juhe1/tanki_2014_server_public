from . import flame_thrower_model_command_handler
from . import flame_thrower_model_commands
from . import flame_thrower_model_data
from client.space.model import Model

class FlameThrowerModel(Model):
    model_id = 300100044

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.model_data = flame_thrower_model_data.FlameThrowerModelData(global_model.get_model_data())
        self.commands = flame_thrower_model_commands.FlameThrowerModelCommands(client_space, game_object)
        self.command_handler = flame_thrower_model_command_handler.FlameThrowerModelCommandHandler(global_model)
