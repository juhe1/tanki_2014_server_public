from space import global_space_registry
from space import global_game_object
from utils.log import console_out
import connection_handler
import server_properties
import threading
import socket

class GlobalSpace:
    def __init__(self, id, name):
        self.id = id
        self.name = name

        self.current_global_game_object_id = server_properties.GLOBAL_GAME_OBJECT_ID_OFFSET # we are using offset, because we dont want that client_game_object and global_game_object ids collide
        self.connecting_clients = [] # clients that are trying to connect to space # TODO: delete connecting client if the client disconnects
        self.client_spaces = []

        self.global_game_objects_by_id = {}
        self.global_game_objects_by_name = {}
        self.global_game_objects_in_loading_order = []

        self.create_default_game_object()

    def remove_space(self):
        global_space_registry.remove_global_space_from_vars(self)

        for global_game_object in self.get_all_global_game_objects():
            global_game_object.remove_global_game_object()

    def get_global_game_object_by_id_or_name(self, global_game_object_id=None, global_game_object_name=None):
        if global_game_object_id:
            return self.get_global_game_object_by_id(global_game_object_id)

        return self.get_global_game_object_by_name(global_game_object_name)

    def remove_global_game_object_from_vars(self, global_game_object):
        if global_game_object == None: return

        global_game_object_id = global_game_object.id

        self.global_game_objects_by_id.pop(global_game_object_id)
        self.global_game_objects_by_name.pop(global_game_object.name)
        self.global_game_objects_in_loading_order.remove(global_game_object)

    def create_default_game_object(self):
        self.add_global_game_object(name="default_game_object", id=self.id)

    def get_default_global_game_object(self):
        return self.global_game_objects_by_id[self.id]

    def get_global_game_object_by_id(self, id):
        if id not in self.global_game_objects_by_id: return
        return self.global_game_objects_by_id[id]

    def get_global_game_object_by_name(self, name):
        if name not in self.global_game_objects_by_name: return
        return self.global_game_objects_by_name[name]

    def get_all_global_game_objects(self):
        return self.global_game_objects_in_loading_order

    def get_global_model(self, model, global_game_object_id=None, global_game_object_name=None):
        global_game_object = self.get_global_game_object_by_id_or_name(global_game_object_id, global_game_object_name)

        if global_game_object == None:
            return

        return global_game_object.get_global_model(model)

    def generate_new_global_game_object_id(self):
        while True:
            self.current_global_game_object_id += 1
            if self.current_global_game_object_id not in self.global_game_objects_by_id: break
        return self.current_global_game_object_id

    def create_global_game_object(self, name, id=None):
        if id == None:
            id = self.generate_new_global_game_object_id()

        if name in self.global_game_objects_by_name.keys():
            name = name + "_" + str(id)

        new_global_game_object = global_game_object.GlobalGameObject(name, id, self)
        return new_global_game_object

    def add_global_game_object_to_dictionarys(self, game_object):
        self.global_game_objects_by_name[game_object.name] = game_object
        self.global_game_objects_by_id[game_object.id] = game_object

    def add_global_game_object(self, name, id=None):
        new_game_object = self.create_global_game_object(name, id)

        self.add_global_game_object_to_dictionarys(new_game_object)
        self.global_game_objects_in_loading_order.append(new_game_object)
        return new_game_object

    # the offset is from end of the list, so 0 offset will add the item to end
    def add_global_game_object_to_order_list_with_offset(self, game_object, offset):
        end = len(self.global_game_objects_in_loading_order)
        self.global_game_objects_in_loading_order.insert(end - offset, game_object)

    def add_global_game_object_with_offset(self, offset, name, id=None):
        new_game_object = self.create_global_game_object(name, id)

        self.add_global_game_object_to_dictionarys(new_game_object)
        self.add_global_game_object_to_order_list_with_offset(new_game_object, offset)

        return new_game_object

    def add_connecting_client(self, client_object):
        self.connecting_clients.append(client_object)

    def add_client_space(self, client_space):
        self.client_spaces.append(client_space)

    def remove_client_space(self, client_space):
        if not client_space in self.client_spaces: return
        self.client_spaces.remove(client_space)

    def try_connecting_new_client(self, client_object, socket, address):
        if not client_object in self.connecting_clients:
            return False

        self.connecting_clients.remove(client_object)
        console_out.log_print(f"client connected to {self.name}_space from {address}")
        client_object.client_space_registry.create_space(self.id, self.name, socket)

        return True
