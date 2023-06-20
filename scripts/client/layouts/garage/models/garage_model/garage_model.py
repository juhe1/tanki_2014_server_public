from client.layouts.garage.models.upgrade_garage_item_model import upgrade_garage_item_model
from client.layouts.lobby.models.lobby_layout_notify_model import lobby_layout_notify_model
from client.layouts.lobby.models.upgrading_items_model import upgrading_items_model
from client.layouts.garage.models.garage_model import garage_model_command_handler
from client.layouts.lobby.models.user_property_model import user_property_model
from client.layouts.garage.models.garage_model import garage_model_commands
from client.layouts.garage.models.garage_model import garage_model_data
from client.layouts.lobby.models.panel_model import panel_model
from client.dispatcher.dispatcher_model import dispatcher_model
from client.layouts.garage.models.item_model import item_model
from loaders.garage_item_loader import garage_item_loader
from client.space import game_object
from client.space.model import Model
from database import garage_tables

import threading
import time
import gc

class GarageModel(Model):
    model_id = 300040008

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.model_data = garage_model_data.GarageModelData(game_object, client_object)
        self.commands = garage_model_commands.GarageModelCommands(client_space, game_object)
        self.command_handler = garage_model_command_handler.GarageModelCommandHandler(client_object)

        self.all_items = {}
        self.all_loaded_item_ids = []
        self.depot_items = []
        self.market_items = []
        self.mounted_items = {"weapon":0, "armor":0, "color":0}

        self.item_game_objects_groups = {"normal_items":[], "kit_items":[]} # so first it will load normal_items and then kit items

    def init_done(self):
        self.game_object.add_model(dispatcher_model.DispatcherModel)
        self.game_object.add_model(upgrade_garage_item_model.UpgradeGarageItemModel)
        self.game_object.load_object_from_client()

        self.load_all_items()
        self.init_client_garage()
        self.mount_all_items_from_client()

        # end layout switch from client
        _lobby_layout_notify_model = self.client_object.client_space_registry.get_model(space_name="lobby", game_object_name="default_game_object", model=lobby_layout_notify_model.LobbyLayoutNotifyModel)
        _lobby_layout_notify_model.end_layout_switch()

    def mount_all_items_from_client(self):
        # mount all items from garage viewer (garage viewer = the thing that shows garage, tank and turret 3d models)
        for item_game_object_id in self.mounted_items.values():
            item_game_object = self.client_space.get_game_object_by_id(item_game_object_id)
            item_item_model = item_game_object.get_model(item_model.ItemModel)
            item_item_model.mount_item()

    def load_all_items(self):
        _user_property_model = self.client_object.client_space_registry.get_model(user_property_model.UserPropertyModel, game_object_name="panel", space_name="lobby")
        user_roles = _user_property_model.model_data.get_user_roles()
        garage_items = garage_item_loader.get_all_items_for_role(user_roles)

        for garage_item_object in garage_items:
            self.load_item(garage_item_object)

        self.load_items_from_client()

    def init_client_garage(self):
        self.commands.init_depot(self.depot_items)
        self.commands.init_mounted(self.mounted_items.values()) # this only mounts the items from gui
        self.commands.init_market(self.market_items)

    def mount_item(self, item_game_object_id, type):
        self.mounted_items[type] = item_game_object_id

        item_game_object = self.client_space.get_game_object_by_id(item_game_object_id)
        item_item_model = item_game_object.get_model(item_model.ItemModel)
        self.client_object.database_garage_item_loader.set_mount(type, item_item_model.item_id)

    def get_item_game_object_by_item_id(self, item_id):
        if item_id in self.all_items:
            return self.all_items[item_id]
        return None

    def load_item(self, garage_item_object):
        if garage_item_object.id in self.all_loaded_item_ids: return

        # create item game object for the item
        name = garage_item_object.name + str(garage_item_object.id) # we add id, because there is items that have same name
        item_game_object = self.client_space.add_game_object(game_object_name=name, game_object_id=100 + garage_item_object.id) # we add 100 to the id because we need to leave lower ids for othe game objects
        item_game_object.add_model(item_model.ItemModel, model_args=(garage_item_object,))

        # add item to all_items, because we need to acces it in kit model
        self.all_items[garage_item_object.id] = item_game_object
        self.all_loaded_item_ids.append(garage_item_object.id)

        if garage_item_object.kit_image: # if item has kit image then it it kit item
            self.item_game_objects_groups["kit_items"].append(item_game_object)
        else:
            self.item_game_objects_groups["normal_items"].append(item_game_object)

        return garage_item_object

    def load_items_from_client(self):
        dispatcher_game_object = self.client_space.get_default_game_object()
        dispatcher_model_commands = dispatcher_game_object.get_model(dispatcher_model.DispatcherModel).commands

        # we want to load items in groups, because for example items that kit countains need to be loaded first. And upgradable items need to be loaded same time
        for item_game_objects in self.item_game_objects_groups.values():
            item_structs = [item_game_object.get_object_struct() for item_game_object in item_game_objects] # generate list of structs from list of game objects
            dispatcher_model_commands.load_objects(item_structs)
        self.item_game_objects_groups = {"normal_items":[], "kit_items":[]}
