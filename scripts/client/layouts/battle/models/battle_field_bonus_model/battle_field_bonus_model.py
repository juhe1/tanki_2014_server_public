from client.layouts.battle.models.battle_field_bonus_model import battle_field_bonus_model_command_handler
from client.layouts.battle.models.battle_field_bonus_model import battle_field_bonus_model_commands
from client.layouts.battle.models.battle_field_bonus_model import battle_field_bonus_model_data
from client.space.model import Model

class BattleFieldBonusModel(Model):
    model_id = 300100007

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.model_data = battle_field_bonus_model_data.BattleFieldBonusModelData(game_object, global_model.get_model_data())
        self.commands = battle_field_bonus_model_commands.BattleFieldBonusModelCommands(client_space, game_object)
        self.command_handler = battle_field_bonus_model_command_handler.BattleFieldBonusModelCommandHandler(global_model, client_object.user_id)
