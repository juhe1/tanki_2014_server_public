from client.dispatcher.dispatcher_model import load_object_struct
from client.dispatcher.dispatcher_model import dispatcher_model
from client.dispatcher.dispatcher_model import model_data
from utils.binary.codecs import basic_codecs
from utils.log import console_out
from utils import list_utils

#from client.layouts.battle.models.battle_field_model import battle_field_model

import weakref
import time

class GameObject:
    def __init__(self, client_object, name):
        self.client_object = client_object
        self.global_game_object = None
        self.name = name
        self.id = 0
        self.space = None

        self.removed = False
        self.loaded = False
        self.models = {}
        self.loaded_model_ids = []
        self.dispatcher_model_commands = None

    def remove_game_object(self):
        for model in self.models.values():
            if model.global_model == None: continue
            model.global_model.remove_client_model(model)

        self.unload_object_from_client()

        self.models = {}
        self.loaded_model_ids = []

        if self.global_game_object:
            self.global_game_object.remove_client_game_object(self)

        self.space.delete_game_object_from_vars(self)
        self.removed = True

    def add_model(self, model, model_args=None, global_model=None):
        if model in self.models:
            return

        args = []
        if model_args:
            args += list(model_args)
        if global_model:
            args.append(global_model)

        new_model = model(self, self.space, self.client_object, *args)
        self.models[model] = new_model

        # run main
        new_model.init_done()

        return new_model

    def add_global_model(self, global_model):
        new_model = self.add_model(global_model.CLIENT_MODEL, global_model=global_model)
        if new_model == None: return
        global_model.register_client_model(new_model)

    def get_model(self, model):
        if not model in self.models: return None
        weak_object = weakref.ref(self.models[model])
        weak_object = weak_object()
        return weak_object

    def model_class_exist(self, model):
        return model in self.models

    def handle_command(self, binary_data):
        command_id = basic_codecs.LongCodec.decode(binary_data)

        console_out.safe_print("recived command id: " + str(command_id))

        for model in self.models.values():
            model_command_handler = model.command_handler
            if model_command_handler == None: continue
            if model_command_handler.handle_command(binary_data, command_id): break # if returns true then break

    def unload_models_from_client(self, models):
        new_models_list = [model for model in self.models if not model in models] # self.models, but without models that we want to unload
        self.load_models_from_client(new_models_list)

    def unload_object_from_client(self):
        if self.dispatcher_model_commands == None:
            dispatcher_object = self.space.get_default_game_object()
            self.dispatcher_model_commands = dispatcher_object.get_model(dispatcher_model.DispatcherModel).commands

        self.dispatcher_model_commands.unload_objects([self.id])

    def get_object_struct(self, models=None):
        if models == None:
            models = self.models.values()

        list_of_models = list( models )
        class_id = self.client_object.game_class_registry.create_class_from_models_and_chost_model(list_of_models)

        model_datas = []
        for model in list_of_models:
            if model.model_data == None: continue
            #if model.model_id in self.loaded_model_ids: continue

            model_data = model.model_data.get_model_data()
            model_datas.append(model_data)
            if not model.model_id in self.loaded_model_ids:
                self.loaded_model_ids.append(model.model_id)

        object_struct = load_object_struct.LoadObjectStruct()
        object_struct.data = model_datas
        object_struct.id = self.id
        object_struct.parent = class_id
        return object_struct

    def load_models_from_client(self, models):
        if not list_utils.items_in_list(models, self.models.keys()): return
        models = [self.models[model] for model in models]

        if self.dispatcher_model_commands == None:
            dispatcher_object = self.space.get_default_game_object()
            self.dispatcher_model_commands = dispatcher_object.get_model(dispatcher_model.DispatcherModel).commands

        object_struct = self.get_object_struct(models)
        self.dispatcher_model_commands.load_objects([object_struct])

    # load this object from client side
    def load_object_from_client(self):
        if self.dispatcher_model_commands == None:
            dispatcher_object = self.space.get_default_game_object()
            self.dispatcher_model_commands = dispatcher_object.get_model(dispatcher_model.DispatcherModel).commands

        object_struct = self.get_object_struct()
        self.dispatcher_model_commands.load_objects([object_struct])

        for new_model in self.models.values():
            # run loaded_from_client
            new_model.loaded_from_client()

        self.loaded = True
