from client.layouts.lobby.models.uid_notifier_model import uid_notifier_model
from . import battle_dm_info_model_command_handler
from . import battle_dm_info_model_commands
from . import battle_dm_info_model_data
from client.space.model import Model

class BattleDmInfoModel(Model):
    model_id = 300090003

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.model_data = battle_dm_info_model_data.BattleDmInfoModelData(game_object, global_model.get_model_data())
        self.commands = battle_dm_info_model_commands.BattleDmInfoModelCommands(client_space, game_object)
        self.command_handler = battle_dm_info_model_command_handler.BattleDmInfoModelCommandHandler(client_object, global_model.get_battle_field_global_space())

        # TODO: load uid_notifier_model and rank_notifier_model
