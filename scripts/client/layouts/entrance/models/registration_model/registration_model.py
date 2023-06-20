from client.layouts.entrance.models.registration_model import registration_model_command_handler
from client.layouts.entrance.models.registration_model import registration_model_commands
from client.layouts.entrance.models.registration_model import registration_model_data
from client.space.model import Model

class RegistrationModel(Model):
    model_id = 300020025

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.commands = registration_model_commands.RegistrationModelCommands(client_space, game_object)
        self.command_handler = registration_model_command_handler.RegistrationModelCommandHandler(self)
        self.model_data = registration_model_data.RegistrationModelData(game_object, client_object)
