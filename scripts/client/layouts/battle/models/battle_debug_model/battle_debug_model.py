from . import battle_debug_model_commands
from client.space.model import Model

class BattleDebugModel(Model):
    model_id = 300100003

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.commands = battle_debug_model_commands.BattleDebugModelCommands(client_space, game_object)
