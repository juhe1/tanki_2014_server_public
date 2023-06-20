from utils.log import console_out

# TODO: start using weak references to avoid memory leaks

class GlobalGameObject:
    def __init__(self, name, id, space):
        self.name = name
        self.id = id
        self.global_space = space
        self.models = {}
        self.client_game_objects = []
        self.removed = False

    def __str__(self):
        return f"GlobalGameObject: id={self.id}, name={self.name}, global_space_name={self.global_space.name}"

    def add_global_model(self, model, model_args=None, owner_id=None):
        if model in self.models:
            error_message = "Can't add model, because it is already added."
            console_out.color_print("[ERROR] " + error_message, "red")
            raise Exception(error_message)
            return

        if model_args:
            new_model = model(self, self.global_space, *model_args, owner_id)
        else:
            new_model = model(self, self.global_space, owner_id)

        self.models[model] = new_model
        new_model.init_done()
        return new_model

    def add_client_game_object(self, game_object):
        self.client_game_objects.append(game_object)

    def remove_client_game_object(self, game_object):
        self.client_game_objects.remove(game_object)

    def remove_global_game_object_from_clients(self):
        for client_game_object in self.client_game_objects.copy():
            client_game_object.remove_game_object()

    def remove_global_game_object(self):
        if self.removed: return
        self.removed = True
        
        self.global_space.remove_global_game_object_from_vars(self)
        self.remove_global_game_object_from_clients()

    def get_global_model(self, model):
        if model in self.models:
            return self.models[model]

    def get_all_global_models(self):
        return self.models.values()

    def clone_to_clients(self):
        for client_space in self.global_space.client_spaces:
            client_space.add_global_game_object(self)

    def load_object_from_clients(self):
        for client_game_object in self.client_game_objects.copy():
            if client_game_object == None: continue
            client_game_object.load_object_from_client()
