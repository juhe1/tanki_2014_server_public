class GlobalModel:
    def __init__(self, global_game_object, global_space, owner_id):
        self.global_game_object = global_game_object
        self.global_space = global_space
        self.owner_id = owner_id

        self.client_models = []

    def register_client_model(self, client_model):
        self.client_models.append(client_model)

    def remove_client_model(self, client_model):
        self.client_models.remove(client_model)

    def is_owner(self, user_id):
        return self.get_owner_id() == user_id

    def get_owner_id(self):
        return self.owner_id

    def get_model_data(self):
        return None

    def get_all_client_models(self):
        return self.client_models

    def broadcast_command(self, command_name, args=()):
        for client_model in self.client_models:
            command = getattr(client_model.commands, command_name)
            command(*args)

    def broadcast_command_only_to_other_players(self, command_name, args=()):
        for client_model in self.client_models:
            if self.is_owner(client_model.client_object.user_id): continue
            command = getattr(client_model.commands, command_name)
            command(*args)

    # this function will be run after the model is created and added to global game object
    def init_done(self):
        return

    # this function will be called when the model is removed
    def removed(self):
        return
