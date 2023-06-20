from client.layouts.lobby.models.upgrading_items_model import upgrading_items_model_command_handler
from client.layouts.lobby.models.upgrading_items_model import upgrading_items_model_commands
from client.layouts.garage.models.data_owner_model import data_owner_model
from client.layouts.garage.codec_data_structs import garage_item_info
from loaders.client_resource_loader import client_resource_loader
from client.space.model import Model
from client.space import game_object
from database import garage_tables

import datetime

class UpgradingItemsModel(Model):
    model_id = 300050067

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.model_data = None
        self.commands = upgrading_items_model_commands.UpgradingItemsModelCommands(client_space, game_object)
        self.command_handler = upgrading_items_model_command_handler.UpgradingItemsModelCommandHandler(client_object, client_space, self)

        self.upgrading_items = []
        self.upgraded_items = []
        self.upgrading_item_game_object_ids_to_item_id = {}

    def init_done(self):
        self.init_upgrading_and_upgraded_items()

    def add_upgrading_item(self, item_game_object_id, item_id):
        self.upgrading_item_game_object_ids_to_item_id[item_game_object_id] = item_id

    def get_and_delete_upgrading_item_id(self, item_game_object_id):
        if not item_game_object_id in self.upgrading_item_game_object_ids_to_item_id: return

        item_id = self.upgrading_item_game_object_ids_to_item_id[item_game_object_id]
        self.upgrading_item_game_object_ids_to_item_id[item_game_object_id] = None

        return item_id

    def finish_upgrade(self, database_garage_item):
        upgrading_property_id = database_garage_item.upgrading_property_id
        database_garage_item.upgradable_property_data_levels[upgrading_property_id] += 1

        database_garage_item.upgrade_done_time = None
        database_garage_item.upgrading_property_id = None
        garage_tables.edit_item(database_garage_item, self.client_object.user_id)

    def init_upgrading_and_upgraded_items(self):
        mounted_items = self.client_object.database_garage_item_loader.get_mounted_items()

        # loop all upgrading items
        for database_garage_item in self.client_object.database_garage_item_loader.get_all_items():
            if database_garage_item.upgrading_property_id == None: continue

            garage_item = database_garage_item.garage_item

            # add panel_object to lobby space. add panel_model and user_property_model to panel_object
            upgrading_item_game_object = self.client_space.add_game_object(game_object_name=name)
            upgrading_item_game_object.add_model(data_owner_model.DataOwnerModel, model_args=(garage_item.data_owner_id,))
            upgrading_item_game_object.load_object_from_client()

            _garage_item_info = garage_item_info.GarageItemInfo()

            datetime_now = datetime.datetime.now()
            remaining_time_in_ms = (database_garage_item.upgrade_done_time - datetime_now).seconds * 1000

            _garage_item_info.category = garage_item.item_category
            _garage_item_info.item = upgrading_item_game_object.id
            _garage_item_info.modification_index = garage_item.modification_index
            _garage_item_info.mounted = garage_item.id in mounted_items.values()
            _garage_item_info.name = garage_item.name
            _garage_item_info.position = garage_item.position
            _garage_item_info.preview = client_resource_loader.get_resource_id(garage_item.preview_image)
            _garage_item_info.remaining_time_in_ms = remaining_time_in_ms

            if database_garage_item.upgrade_done_time < datetime_now:
                self.finish_upgrade(database_garage_item)
                _garage_item_info.remaining_time_in_ms = 0
                self.upgraded_items.append(_garage_item_info)
                return

            self.add_upgrading_item(upgrading_item_game_object.id, garage_item.id)
            self.upgrading_items.append(_garage_item_info)

    def init(self):
        self.commands.init(self.upgraded_items, self.upgrading_items)
