from . import chat_model_command_handler
from client.space.model import Model
from . import chat_model_commands

class ChatModel(Model):
    model_id = 300100022

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.model_data = None
        self.commands = chat_model_commands.ChatModelCommands(client_space, game_object)
        self.command_handler = chat_model_command_handler.ChatModelCommandHandler()
