from . import settings_model_command_handler
from . import settings_model_commands
from client.space.model import Model

class SettingsModel(Model):
    model_id = 300050057

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.model_data = None
        self.commands = settings_model_commands.SettingsModelCommands(client_space, game_object)
        self.command_handler = settings_model_command_handler.SettingsModelCommandHandler(self)
