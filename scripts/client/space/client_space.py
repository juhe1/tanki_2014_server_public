from client.dispatcher.dispatcher_model import dispatcher_model
from utils.binary.codecs import basic_codecs
from space import global_space_registry
from utils.binary import binary_stream
from utils.binary import binary_buffer
from client.space import game_object
from utils.log import console_out
import server_properties

import threading
import weakref
import random
import socket

class ClientSpace:
    def __init__(self, client_object, id, name, socket):
        self.client_object = client_object
        self.id = id
        self.name = name
        self.socket = socket

        self.game_objects_by_id = {}
        self.game_objects_by_name = {}
        self.game_objects_in_loading_order = []

        self.newest_object_id = id # we want that the first real object id is larger than default objects id
        self.space_is_running_flag = True
        self.global_space = global_space_registry.get_space_by_id(id)

        self.create_default_game_object()
        self.create_command_reciver_thread()

    def create_default_game_object(self):
        default_game_object = self.add_game_object(game_object_name="default_game_object", game_object_id=self.id) # in every space there is default game object. the default game object id and the space id is same
        default_game_object.add_model(dispatcher_model.DispatcherModel)

    def load_unloaded_game_objects_from_client(self):
        for game_object in self.get_all_unloaded_game_objects():
            game_object.load_object_from_client()

    def remove_all_game_objects(self):
        for _game_object in self.get_all_game_objects():
            if _game_object.id == self.id: continue # dont unload default game_object yet, because there is dispatcher_model and we need it for unloading game_objects from client
            _game_object.remove_game_object()

        # delete default game_object last
        self.get_default_game_object().remove_game_object()

    def remove_space(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.space_is_running_flag = False

        self.global_space.remove_client_space(self)
        self.remove_all_game_objects()
        self.client_object.client_space_registry.remove_space_from_vars(self)

    def generate_new_game_object_id(self):
        self.newest_object_id += 1

        if self.newest_object_id in self.game_objects_by_id:
            self.newest_object_id += 1

        return self.newest_object_id

    def print_game_object_id_error(self):
        error_message = "game object with id: " + str(game_object_id) + " already exist"
        raise Exception(error_message)
        console_out.color_print("[ADD_GAME_OBJECT][ERROR] " + error_message, "red")

    def create_game_object(self, game_object_name, game_object_id=None):
        new_game_object = game_object.GameObject(self.client_object, game_object_name)

        if game_object_id == None:
            game_object_id = self.generate_new_game_object_id()

        if new_game_object.name in self.game_objects_by_name:
            new_game_object.name = new_game_object.name + " " + str(self.newest_object_id)

        if game_object_id in self.game_objects_by_id:
            self.print_game_object_id_error(game_object_id)
            return

        new_game_object.space = self
        new_game_object.id = game_object_id

        return new_game_object

    def add_game_object_to_dictionarys(self, game_object):
        self.game_objects_by_name[game_object.name] = game_object
        self.game_objects_by_id[game_object.id] = game_object

    def add_game_object(self, game_object_name, game_object_id=None):
        new_game_object = self.create_game_object(game_object_name, game_object_id)

        self.add_game_object_to_dictionarys(new_game_object)
        self.game_objects_in_loading_order.append(new_game_object)
        return new_game_object

    # the offset is from end of the list, so 0 offset will add the item to end
    def add_game_object_to_order_list_with_offset(game_object, offset):
        end = len(self.game_objects_in_loading_order)
        self.game_objects_in_loading_order.insert(end - offset, game_object)

    def add_game_object_with_offset(self, game_object_name, game_object_id=None):
        new_game_object = self.create_game_object(game_object_name, game_object_id)

        self.add_game_object_to_dictionarys(new_game_object)
        self.add_game_object_to_order_list_with_offset(new_game_object, offset)
        return new_game_object

    def update_global_game_object(self, global_game_object):
        _game_object = self.get_game_object_by_id(global_game_object.id)
        _game_object.global_game_object = global_game_object

        for global_model in global_game_object.get_all_global_models():
            if _game_object.model_class_exist(global_model.CLIENT_MODEL): continue
            _game_object.add_global_model(global_model)

    def add_global_game_object(self, global_game_object):
        if global_game_object.id in self.game_objects_by_id:
            _game_object = self.get_game_object_by_id(global_game_object.id)
        else:
            _game_object = self.add_game_object(global_game_object.name, global_game_object.id)

        for global_model in global_game_object.get_all_global_models():
            _game_object.add_global_model(global_model)

        global_game_object.add_client_game_object(_game_object)
        _game_object.global_game_object = global_game_object
        return _game_object

    def clone_game_object_from_global_space(self, game_object_name=None, game_object_id=None):
        if game_object_name:
            global_game_object = self.global_space.get_global_game_object_by_name(game_object_name)
        else:
            global_game_object = self.global_space.get_global_game_object_by_id(game_object_id)

        return self.add_global_game_object(global_game_object)

    def game_object_id_exist(self, game_object_id):
        if game_object_id in self.game_objects_by_id:
            return True
        return False

    def get_game_object_by_name(self, name):
        if not name in self.game_objects_by_name: return None
        weak_object = weakref.ref(self.game_objects_by_name[name])
        weak_object = weak_object()
        return weak_object

    def get_game_object_by_id(self, id):
        if not id in self.game_objects_by_id: return None
        weak_object = weakref.ref(self.game_objects_by_id[id])
        weak_object = weak_object()
        return weak_object

    def get_all_unloaded_game_objects(self):
        game_objects = self.get_all_game_objects()
        return [game_object for game_object in game_objects if not game_object.loaded]

    def get_all_game_objects(self):
        return self.game_objects_in_loading_order

    def get_default_game_object(self):
        return self.game_objects_by_id[self.id] # we use space id, because space has same id as the default_game_object

    def get_model(self, model, game_object_name=None, game_object_id=None):
        if game_object_name:
            _game_object = self.get_game_object_by_name(game_object_name)
        if game_object_id:
            _game_object = self.get_game_object_by_id(game_object_id)
        if _game_object == None:
            return
        return _game_object.get_model(model)

    def delete_game_object_from_vars(self, game_object):
        if game_object == None or game_object.removed: return
        self.game_objects_by_id.pop(game_object.id)
        self.game_objects_by_name.pop(game_object.name)
        self.game_objects_in_loading_order.remove(game_object)

    def send_command(self, object_id, command_buffer, command_name="command_name_not_defined"):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(object_id, buffer)
        buffer.merge_buffer(command_buffer)
        basic_codecs.PackageCodec.encode(buffer)

        console_out.print_server_package(buffer, command_name)

        try:
            self.socket.sendall(buffer.get_binary_data())
        except socket.error:
            return

    def create_command_reciver_thread(self):
        thread = threading.Thread(target=self.recive_commands, args=())
        thread.start()

    def recive_commands(self):
        while True:
            try:
                data = self.socket.recv(server_properties.RECEIVE_BUFFER_SIZE) # recive data from client
            except:
                return

            if data == b"": return # if we dont recive anything then client is disconnected so we can stop reciving
            if self.space_is_running_flag == False: return

            # write client package to screen
            if server_properties.DEBUG_ENABLED:
                console_out.print_command(data, self.name)

            binary_data = binary_stream.BinaryStream(data)
            binary_datas = basic_codecs.PackageCodec.decode(binary_data)

            for binary_data in binary_datas:
                object_id = basic_codecs.LongCodec.decode(binary_data)
                object = self.get_game_object_by_id(object_id)

                if object != None:
                    object.handle_command(binary_data)
