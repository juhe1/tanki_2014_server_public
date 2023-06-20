from . import freeze_model_command_handler
from . import freeze_model_commands
from . import freeze_model_data
from client.space.model import Model

class FreezeModel(Model):
    model_id = 300100046

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.model_data = freeze_model_data.FreezeModelData(global_model.get_model_data())
        self.commands = freeze_model_commands.FreezeModelCommands(client_space, game_object)
        self.command_handler = freeze_model_command_handler.FreezeModelCommandHandler(global_model)
