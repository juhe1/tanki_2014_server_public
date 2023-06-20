from client.layouts.battle_list.models.battle_create_model import battle_create_model_command_handler
from client.layouts.battle_list.models.battle_create_model import battle_create_model_commands
from client.layouts.battle_list.models.battle_create_model import battle_create_model_data
from client.layouts.battle_list.models.battle_select_model import battle_select_model
from client.space.model import Model

class BattleCreateModel(Model):
    model_id = 300090002

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        _battle_select_model = game_object.get_model(battle_select_model.BattleSelectModel)

        self.model_data = battle_create_model_data.BattleCreateModelData(game_object, client_object)
        self.commands = battle_create_model_commands.BattleCreateModelCommands(client_space, game_object)
        self.command_handler = battle_create_model_command_handler.BattleCreateModelCommandHandler(self, _battle_select_model, client_object)
