from . import statistics_team_model_commands
from . import statistics_team_model_data
from client.space.model import Model

class StatisticsTeamModel(Model):
    model_id = 300080033

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.model_data = statistics_team_model_data.StatisticsTeamModelData(global_model.get_model_data())
        self.commands = statistics_team_model_commands.StatisticsTeamModelCommands(client_space, game_object)
