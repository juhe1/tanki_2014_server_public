from . import example_model_command_handler
from . import example_model_commands
from . import example_model_data
from client.space.model import Model

class ExampleModel(Model):
    model_id = 999999999999999

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.model_data = example_model_data.ExampleModelData()
        self.commands = example_model_commands.ExampleModelCommands(client_space, game_object)
        self.command_handler = example_model_command_handler.ExampleModelCommandHandler()
