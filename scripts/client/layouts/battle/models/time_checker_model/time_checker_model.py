from . import time_checker_model_command_handler
from . import time_checker_model_commands
from client.space.model import Model

class TimeCheckerModel(Model):
    model_id = 300100088

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.model_data = None
        self.commands = time_checker_model_commands.TimeCheckerModelCommands(client_space, game_object)
        self.command_handler = time_checker_model_command_handler.TimeCheckerModelCommandHandler()
