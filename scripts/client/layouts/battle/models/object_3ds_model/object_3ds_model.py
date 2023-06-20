from . import object_3ds_model_data
from client.space.model import Model

class Object3DSModel(Model):
    model_id = 300040017

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.model_data = object_3ds_model_data.Object3DSModelData(game_object, client_object, global_model._3ds_resource_name)
        self.commands = None
        self.command_handler = None
