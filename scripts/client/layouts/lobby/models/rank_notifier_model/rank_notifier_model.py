from . import rank_notifier_model_commands
from . import rank_notifier_model_data
from client.space.model import Model

class RankNotifierModel(Model):
    model_id = 300150003

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.model_data = rank_notifier_model_data.RankNotifierModelData(game_object, client_object)
        self.commands = rank_notifier_model_commands.RankNotifierModelCommands(client_space, game_object)
        self.command_handler = None

    def loaded_from_client(self):
        self.global_model.set_ranks()
