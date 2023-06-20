from client.layouts.battle_list.models.team_battle_item_model import team_battle_item_model_commands
from client.layouts.battle_list.models.team_battle_item_model import team_battle_item_model_data
from client.space.model import Model

class TeamBattleItemModel(Model):
    model_id = 300090028

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)
        team_battle_item_model_cc = global_model.get_model_data()

        self.model_data = team_battle_item_model_data.TeamBattleItemModelData(game_object, team_battle_item_model_cc)
        self.commands = team_battle_item_model_commands.TeamBattleItemModelCommands(client_space, game_object)
        self.command_handler = None
