from . import statistics_model_command_handler
from . import statistics_model_commands
from client.space.model import Model
from . import statistics_model_data

class StatisticsModel(Model):
    model_id = 300080032

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.model_data = statistics_model_data.StatisticsModelData(game_object, client_object, global_model)
        self.commands = statistics_model_commands.StatisticsModelCommands(client_space, game_object)
        self.command_handler = statistics_model_command_handler.StatisticsModelCommandHandler()
