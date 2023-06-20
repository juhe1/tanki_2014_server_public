from client.layouts.battle_list.models.battle_info_model import battle_info_model_command_handler
from client.layouts.battle_list.models.battle_info_model import battle_info_model_commands
from client.layouts.battle_list.models.battle_info_model import battle_info_model_data
from client.space.model import Model

class BattleInfoModel(Model):
    model_id = 300090007

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        battle_info_model_cc = global_model.get_model_data()

        self.model_data = battle_info_model_data.BattleInfoModelData(game_object, client_object, client_space, battle_info_model_cc)
        self.commands = battle_info_model_commands.BattleInfoModelCommands(client_space, game_object)
        self.command_handler = battle_info_model_command_handler.BattleInfoModelCommandHandler()
