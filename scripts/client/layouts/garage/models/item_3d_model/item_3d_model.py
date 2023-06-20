from client.space.model import Model

class Item3DModel(Model):
    model_id = 300040009

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.model_data = None
        self.commands = None
        self.command_handler = None
