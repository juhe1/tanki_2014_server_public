from . import uid_notifier_model_commands
from . import uid_notifier_model_data
from client.space.model import Model

class UidNotifierModel(Model):
    model_id = 300150005

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.model_data = uid_notifier_model_data.UidNotifierModelData(game_object, client_object)
        self.commands = uid_notifier_model_commands.UidNotifierModelCommands(client_space, game_object)
        self.command_handler = None

    def loaded_from_client(self):
        self.global_model.set_uids()
