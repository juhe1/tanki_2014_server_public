from . import user_notifier_model_command_handler
from . import user_notifier_model_data
from client.space.model import Model

class UserNotifierModel(Model):
    model_id = 300150006

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.model_data = user_notifier_model_data.UserNotifierModelData(game_object, client_object)
        self.commands = None
        self.command_handler = user_notifier_model_command_handler.UserNotifierModelCommandHandler()
