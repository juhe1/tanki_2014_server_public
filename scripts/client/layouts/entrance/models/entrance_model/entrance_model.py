from client.layouts.entrance.models.registration_model import registration_model
from client.layouts.entrance.models.entrance_model import entrance_model_data
from client.layouts.entrance.models.login_model import login_model
from client.space.model import Model

import threading
import time

class EntranceModel(Model):
    model_id = 300020011

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.model_data = entrance_model_data.EntranceModelData(game_object, client_object)
        self.commands = None
        self.command_handler = None

    def init_done(self):
        # load resources
        self.client_object.resource_loader.load_resource("entrance\\", language=self.client_object.language)
        self.client_object.resource_loader.load_resource("lobby\\", language=self.client_object.language)
        self.client_object.resource_loader.load_resource("garage\\", language=self.client_object.language)
        self.client_object.resource_loader.load_resource("shared\\tank_parts", language=self.client_object.language)

        # TODO: make remember me system and dont execute these lines bellow this command if user logs with remember me
        self.game_object.add_model(login_model.LoginModel)
        self.game_object.add_model(registration_model.RegistrationModel)
        self.game_object.load_object_from_client()
