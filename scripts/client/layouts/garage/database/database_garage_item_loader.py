from client.layouts.garage.database import database_garage_item
from loaders.garage_item_loader import garage_item_loader
from database import garage_tables
import server_properties

class DatabaseGarageItemLoader:
    def __init__(self):
        self.mounted_items = None
        self.items = None

    def load_items(self, user_id):
        self.mounted_items = garage_tables.get_mounted_items_from_database(user_id)
        self.items = garage_tables.get_items_from_data_base(user_id)

        # create starting items, if we dont have any items
        if len(self.items) == 0:
            self.create_starting_items(user_id)

    def create_starting_items(self, user_id):
        for item_id in server_properties.STARTING_ITEM_IDS:
            garage_item = garage_item_loader.get_item_by_id(item_id)
            database_garage_item = self.create_new_database_garage_item(garage_item)
            database_garage_item.count = 1

            garage_tables.add_item(database_garage_item, user_id)
            garage_tables.mount_item(database_garage_item, garage_item.item_category, user_id)
            self.set_mount(garage_item.item_category, item_id)

    def get_mounted_items(self):
        return self.mounted_items

    def get_all_items(self):
        return self.items.values()

    def set_mount(self, item_type, item_id):
        self.mounted_items[item_type] = item_id

    def get_item_by_base_id(self, base_id):
        garage_items = garage_item_loader.get_items_by_base_id(base_id)
        for garage_item in garage_items:
            if not garage_item.id in self.items: continue
            return self.items[garage_item.id]

    def create_new_database_garage_item(self, garage_item):
        item = database_garage_item.DatabaseGarageItem(garage_item)
        item.item_id = garage_item.id

        if garage_item.upgradable_property_datas != None:
            for property_data in garage_item.upgradable_property_datas:
                property_data_id = property_data.property_id
                item.upgradable_property_data_levels[property_data_id] = property_data.level

        if garage_item.modification_index != None:
            item.modification_index = garage_item.modification_index

        if garage_item.temporary_item_life_time_in_sec != None:
            time_now = datetime.datetime.now()
            temporary_item_life_time = garage_item.temporary_item_life_time_in_sec
            item.temporary_item_expiration_time = time_now + datetime.timedelta(0, temporary_item_life_time)

        self.items[item.item_id] = item
        return item

    def get_item_by_id(self, item_id):
        if item_id in self.items:
            return self.items[item_id]
        return None
