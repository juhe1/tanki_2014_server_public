from . import battle_mines_model_commands
from . import battle_mines_model_data
from client.space.model import Model

class BattleMinesModel(Model):
    model_id = 300100006

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.model_data = battle_mines_model_data.BattleMinesModelData(global_model.get_model_data())
        self.commands = battle_mines_model_commands.BattleMinesModelCommands(client_space, game_object)
