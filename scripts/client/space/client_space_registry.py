from client.space import client_space

import time
import weakref

class ClientSpaceRegistry:
    def __init__(self, client_object):
        self.client_object = client_object
        self.space_by_name = {}
        self.space_by_id = {}
        self.updated = False

    # return when space is created
    def wait_for_space(self, space_name):
        while True:
            if self.updated == True: # we do this check becuse we want to get this running more smoothly
                self.updated = False
                if space_name in self.space_by_name:
                    return self.space_by_name[space_name]
            time.sleep(0.1)

    def add_global_space(self, global_space):
        # connect to space
        client_space = self.client_object.basic_commands.open_space(global_space.name)

        # add all global_game_objects to client_space
        for global_game_object in global_space.get_all_global_game_objects():
            client_space.add_global_game_object(global_game_object)

        global_space.add_client_space(client_space)
        return client_space

    def update_global_space(self, global_space):
        client_space = self.get_space_by_id(global_space.id)

        # add all new global_game_objects to client_space
        for global_game_object in global_space.get_all_global_game_objects():

            if client_space.game_object_id_exist(global_game_object.id):
                client_space.update_global_game_object(global_game_object)
                continue

            client_space.add_global_game_object(global_game_object)

        return client_space

    def create_space(self, id, name, socket):
        new_space = client_space.ClientSpace(self.client_object, id, name, socket)
        self.space_by_name[name] = new_space
        self.space_by_id[id] = new_space
        self.updated = True

    def remove_space_from_vars(self, space):
        self.space_by_name.pop(space.name)
        self.space_by_id.pop(space.id)

    def remove_all_spaces(self):
        for space in self.get_all_spaces():
            space.remove_space()

    def get_space_by_name(self, name):
        if not name in self.space_by_name:
            return
        weak_object = weakref.ref(self.space_by_name[name])
        weak_object = weak_object()
        return weak_object

    def get_space_by_id(self, id):
        return self.space_by_id[id]

    def get_all_spaces(self):
        return list(self.space_by_id.values())

    def get_game_object(self, space_name=None, space_id=None, game_object_name=None, game_object_id=None):
        if space_name:
            space = self.get_space_by_name(space_name)
        else:
            space = self.get_space_by_id(space_id)

        if game_object_name:
            return space.get_game_object_by_name(game_object_name)
        else:
            return space.get_game_object_by_id(game_object_id)

    def get_model(self, model, game_object_name=None, game_object_id=None, space_name=None, space_id=None):
        if space_name:
            space = self.get_space_by_name(space_name)
        else:
            space = self.get_space_by_id(space_id)

        if game_object_name:
            game_object = space.get_game_object_by_name(game_object_name)
        else:
            game_object = space.get_game_object_by_id(game_object_id)

        if game_object == None: return None
        return game_object.get_model(model)
