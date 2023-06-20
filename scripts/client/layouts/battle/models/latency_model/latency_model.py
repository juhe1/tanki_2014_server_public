from . import latency_model_command_handler
from . import latency_model_commands
from client.space.model import Model

class LatencyModel(Model):
    model_id = 300080022

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.model_data = None
        self.commands = latency_model_commands.LatencyModelCommands(client_space, game_object)
        self.command_handler = latency_model_command_handler.LatencyModelCommandHandler()
