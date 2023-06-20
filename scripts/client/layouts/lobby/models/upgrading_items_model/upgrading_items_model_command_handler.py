from client.layouts.garage.models.data_owner_model import data_owner_model
from client.layouts.garage.models.garage_model import garage_model
from client.layouts.garage.models.item_model import item_model
from utils.binary.codecs import basic_codecs
from client.space import game_object
from database import garage_tables


class UpgradingItemsModelCommandHandler:
    def __init__(self, client_object, space, _upgrading_items_model):
        self.upgrading_items_model = _upgrading_items_model
        self.space = space
        self.client_object = client_object

        self.ITEM_UPGRADED_COMMAND_ID = 300050051

    def handle_command(self, binary_data, command_id):
        if command_id == self.ITEM_UPGRADED_COMMAND_ID:
            self.item_upgraded(binary_data)
            return True
        return False

    def item_upgraded(self, binary_data):
        item_game_object_id = basic_codecs.LongCodec.decode(binary_data)
        item_id = self.upgrading_items_model.get_and_delete_upgrading_item_id(item_game_object_id)

        database_garage_item = self.client_object.database_garage_item_loader.get_item_by_id(item_id)

        if database_garage_item == None:
            return

        self.upgrading_items_model.finish_upgrade(database_garage_item)
