class Model:
    def __init__(self, game_object, client_space, client_object, global_model):
        self.game_object = game_object
        self.client_space = client_space
        self.client_object = client_object
        self.global_model = global_model

        self.model_data = None
        self.commands = None
        self.command_handler = None

    # this function will be executed after model is addet to game_object
    def init_done(self):
        return

    # this function will be executed after model is loaded from client
    def loaded_from_client(self):
        return
