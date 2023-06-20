from . import team_battle_info_model_command_handler
from . import team_battle_info_model_commands
from . import team_battle_info_model_data
from client.space.model import Model

class TeamBattleInfoModel(Model):
    model_id = 300090027

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.model_data = team_battle_info_model_data.TeamBattleInfoModelData(game_object, global_model.get_model_data())
        self.commands = team_battle_info_model_commands.TeamBattleInfoModelCommands(client_space, game_object)
        self.command_handler = team_battle_info_model_command_handler.TeamBattleInfoModelCommandHandler(client_object, global_model.get_battle_field_global_space())
