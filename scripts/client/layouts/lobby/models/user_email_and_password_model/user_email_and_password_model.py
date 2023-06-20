from . import user_email_and_password_model_command_handler
from . import user_email_and_password_model_commands
from . import user_email_and_password_model_data
from client.space.model import Model

class UserEmailAndPasswordModel(Model):
    model_id = 300050070

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.model_data = user_email_and_password_model_data.UserEmailAndPasswordModelData(game_object, client_object)
        self.commands = user_email_and_password_model_commands.UserEmailAndPasswordModelCommands(client_space, game_object)
        self.command_handler = user_email_and_password_model_command_handler.UserEmailAndPasswordModelCommandHandler()
