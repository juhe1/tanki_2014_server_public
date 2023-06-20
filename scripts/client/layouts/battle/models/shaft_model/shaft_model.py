from . import shaft_model_command_handler
from . import shaft_model_commands
from . import shaft_model_data
from client.space.model import Model

class ShaftModel(Model):
    model_id = 300100066

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.model_data = shaft_model_data.ShaftModelData(global_model.get_model_data())
        self.commands = shaft_model_commands.ShaftModelCommands(client_space, game_object)
        self.command_handler = shaft_model_command_handler.ShaftModelCommandHandler(global_model)
