from client.dispatcher.dispatcher_model import dispatcher_model_commands
from client.space.model import Model

class DispatcherModel(Model):
    model_id = 100001

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.commands = dispatcher_model_commands.DispatcherModelCommands(client_space, game_object)
        self.command_handler = None
        self.model_data = None
