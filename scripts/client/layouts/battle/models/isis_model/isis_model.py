from . import isis_model_command_handler
from . import isis_model_commands
from . import isis_model_data
from client.space.model import Model

class IsisModel(Model):
    model_id = 300100053

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.model_data = isis_model_data.IsisModelData(global_model.get_model_data())
        self.commands = isis_model_commands.IsisModelCommands(client_space, game_object)
        self.command_handler = isis_model_command_handler.IsisModelCommandHandler()
