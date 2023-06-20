from client.layouts.battle_list.models.battle_dm_item_model import battle_dm_item_model_commands
from client.layouts.battle_list.models.battle_dm_item_model import battle_dm_item_model_data
from client.space.model import Model

class BattleDmItemModel(Model):
    model_id = 300090004

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)
        battle_dm_item_model_cc = global_model.get_model_data()

        self.model_data = battle_dm_item_model_data.BattleDmItemModelData(client_object, game_object, battle_dm_item_model_cc)
        self.commands = battle_dm_item_model_commands.BattleDmItemModelCommands(client_space, game_object)
        self.command_handler = None
