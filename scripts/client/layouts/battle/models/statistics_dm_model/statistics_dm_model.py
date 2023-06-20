from client.layouts.lobby.models.user_property_model import user_property_model
from client.layouts.battle.models.statistics_model import statistics_model
from . import statistics_dm_model_commands
from . import statistics_dm_model_data
from client.space.model import Model
import server_properties

class StatisticsDmModel(Model):
    model_id = 300080031

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        user_infos = global_model.get_model_data().user_infos
        self.model_data = statistics_dm_model_data.StatisticsDmModelData(game_object, user_infos)
        self.commands = statistics_dm_model_commands.StatisticsDmModelCommands(client_space, game_object)
        self.command_handler = None
