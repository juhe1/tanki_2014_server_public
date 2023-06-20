from client.layouts.garage.models.upgradeable_params_constructor_model import upgradeable_params_constructor_model
from client.layouts.lobby.models.upgrading_items_model import upgrading_items_model
from client.layouts.garage.models.countable_item_model import countable_item_model
from client.layouts.lobby.models.user_property_model import user_property_model
from client.layouts.garage.models.garage_kit_model import garage_kit_model
from client.layouts.garage.models.buyable_model import buyable_model_data
from client.layouts.garage.models.garage_model import garage_model
from client.layouts.garage.models.item_model import item_model
from loaders.garage_item_loader import garage_item_loader
from client.layouts.garage.garage_utils import name_to_id
from client.space.model import Model
from database import garage_tables
import server_properties

import datetime
import math

class BuyableModel(Model):
    model_id = 300040001

    def __init__(self, game_object, client_space, client_object, garage_item_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.model_data = buyable_model_data.BuyableModelData(game_object, client_object, garage_item_object, client_space, self)
        self.commands = None
        self.command_handler = None

        self.item_model = game_object.get_model(item_model.ItemModel)
        self.garage_item_object = garage_item_object
        self.garage_model = client_space.get_model(garage_model.GarageModel, "default_game_object")

        self.lobby_space = self.client_object.client_space_registry.get_space_by_name("lobby")
        self.user_property_model = self.lobby_space.get_model(user_property_model.UserPropertyModel, game_object_name="panel")
        self.upgrading_items_model = self.lobby_space.get_model(upgrading_items_model.UpgradingItemsModel, game_object_name="panel")
        self.user_id = client_object.user_id

    def kit_bought(self):
        discount = self.garage_item_object.kit_discount

        for kit_item in self.garage_item_object.kit_items:
            item_game_object = self.garage_model.get_item_game_object_by_item_id(kit_item.item)
            item_buyable_model = item_game_object.get_model(BuyableModel)
            garage_item = garage_item_loader.get_item_by_id(kit_item.item)

            current_mod_database_item = None
            if garage_item.base_item_id != None:
                current_mod_database_item = self.client_object.database_garage_item_loader.get_item_by_base_id(garage_item.base_item_id) # get modification database item that user owns of the item that he is trying to buy

            # if user doesnt own modification off the item that he is trying to buy
            if current_mod_database_item == None:
                item_buyable_model.item_bought(kit_item.count, discount)
                return

            current_mod_garage_item = garage_item_loader.get_item_by_id(current_mod_database_item.item_id)
            current_mod_game_object = self.garage_model.get_item_game_object_by_item_id(current_mod_database_item.item_id)
            current_mod_item_model = current_mod_game_object.get_model(item_model.ItemModel)

            if current_mod_garage_item.modification_index <= garage_item.modification_index:
                # buy new modification
                item_buyable_model.item_bought(kit_item.count, discount)
                # delete old modification from user
                current_mod_item_model = current_mod_game_object.get_model(item_model.ItemModel)
                current_mod_item_model.set_user_owns_to_false()

    def buy_next_modification(self, custom_discount=0):
        if self.garage_item_object.modification_index >= 3: return

        # buy next modification
        modification_discount = self.calculate_modification_discount()
        next_modification_game_object = self.item_model.get_next_modification_game_object()
        next_modification_buyable_model = next_modification_game_object.get_model(BuyableModel)
        next_modification_buyable_model.item_bought(0, custom_discount=modification_discount + custom_discount)

        # delete old modification
        self.item_model.set_user_owns_to_false()

    def calculate_modification_discount(self):
        discount = 0
        upgradable_property_data_levels = self.item_model.database_garage_item.upgradable_property_data_levels

        for property_level_key, property_level in upgradable_property_data_levels.items():
            property_data = self.garage_item_object.get_upgradable_property_data_by_id(property_level_key)
            if property_level != property_data.max_level: continue

            all_upgrade_steps_cost = 0
            for x in range(0, property_data.max_level):
                all_upgrade_steps_cost += property_data.cost.calculate_linear_value(x)

            discount += all_upgrade_steps_cost / self.model_data.price_with_discount

        return round(discount, 2)

    def instant_upgrade(self, property_id, num_levels, expected_price):
        real_price = 0
        for x in range(num_levels):
            upgradable_property_data = self.garage_item_object.get_upgradable_property_data_by_id(property_id)

            real_price += self.calculate_upgrade_price(property_id, upgradable_property_data)
            upgrade_time = self.calculate_upgrade_time(property_id, upgradable_property_data)
            real_price += self.calculate_speedup_cost(upgrade_time, upgradable_property_data.speed_up_discount)
            max_level = upgradable_property_data.max_level
            if self.item_model.database_garage_item.upgradable_property_data_levels[property_id] >= max_level: return # if we are in max level then return
            self.item_model.database_garage_item.upgradable_property_data_levels[property_id] += 1

        if not real_price == expected_price or self.user_property_model.model_data.crystals < real_price:
            self.item_model.database_garage_item.upgradable_property_data_levels[property_id] -= num_levels
            # TODO: send some funny troll message and if possible add some funny picture
            return

        garage_tables.edit_item(self.item_model.database_garage_item, self.user_id)
        self.user_property_model.subtract_crystals(real_price)

    def buy_speed_up(self, expected_price):
        upgrading_property_id = self.item_model.database_garage_item.upgrading_property_id
        upgradable_property_data = self.garage_item_object.get_upgradable_property_data_by_id(upgrading_property_id)

        upgrade_time = self.calculate_upgrade_time(upgrading_property_id, upgradable_property_data)
        real_price = self.calculate_speedup_cost(upgrade_time, upgradable_property_data.speed_up_discount)

        if not real_price == expected_price or self.user_property_model.model_data.crystals < real_price:
            # TODO: send some funny troll message and if possible add some funny picture
            return

        self.upgrading_items_model.finish_upgrade(self.item_model.database_garage_item)
        self.user_property_model.subtract_crystals(real_price)

    def calculate_speedup_cost(self, time, discount):
        speed_up_coeff = server_properties.UPGRADE_SPEEDUP_COEFFICIENT
        speed_up_coeff = speed_up_coeff * math.log(10)
        time = time / 60
        price = time * (1 + speed_up_coeff / math.log(time + 10)) * 0.5
        price = math.floor(price + 0.5)
        return self.calculate_value_with_discount(price, discount)

    def upgrade_item(self, property_id, expected_price, expected_time_in_seconds):
        if not property_id in self.item_model.database_garage_item.upgradable_property_data_levels: return # return, if item doesnt have param that we try to upgrade
        if not self.item_model.user_owns_item: return # return, if user doesnt own the item
        if self.item_model.database_garage_item.upgrading_property_id: return # return, if item is upgrading

        upgradable_property_data = self.garage_item_object.get_upgradable_property_data_by_id(property_id)

        level = self.item_model.database_garage_item.upgradable_property_data_levels[property_id]
        if level >= upgradable_property_data.max_level: return  # return, if property is upgradet to max

        real_price = self.calculate_upgrade_price(property_id, upgradable_property_data)
        real_time_in_seconds = self.calculate_upgrade_time(property_id, upgradable_property_data)

        if not real_price == expected_price or self.user_property_model.model_data.crystals < real_price or not expected_time_in_seconds == real_time_in_seconds:
            # TODO: send some funny troll message and if possible add some funny picture
            return

        self.user_property_model.subtract_crystals(real_price)

        time_now = datetime.datetime.now()
        self.item_model.database_garage_item.upgrade_done_time = time_now + datetime.timedelta(0,real_time_in_seconds)
        self.item_model.database_garage_item.upgrading_property_id = property_id
        garage_tables.edit_item(self.item_model.database_garage_item, self.user_id)

        self.upgrading_items_model.add_upgrading_item(self.game_object.id, self.garage_item_object.id)

    def calculate_upgrade_price(self, property_id, upgradable_property_data):
        level = self.item_model.database_garage_item.upgradable_property_data_levels[property_id]
        linear_param_price = upgradable_property_data.cost

        price = linear_param_price.calculate_linear_value(level)
        price = self.calculate_value_with_discount(price, upgradable_property_data.upgrade_discount)
        return price

    def calculate_upgrade_time(self, property_id, upgradable_property_data):
        level = self.item_model.database_garage_item.upgradable_property_data_levels[property_id]
        linear_param_time = upgradable_property_data.time

        time_in_seconds = linear_param_time.calculate_linear_value(level) * 60
        time_in_seconds = self.calculate_value_with_discount(time_in_seconds, upgradable_property_data.time_discount)
        return time_in_seconds

    def calculate_value_with_discount(self, value, discount):
        value_with_discount = value * (100 - discount) * 0.01 + 0.001
        return math.floor(value_with_discount)

    def calculate_item_price(self, count, custom_discount=0):
        price_with_discount = self.model_data.price_with_discount - (custom_discount * self.model_data.price_with_discount)
        real_price = price_with_discount * count
        return real_price

    def item_bought(self, count, custom_discount=0, expected_price=False):
        if count == 0: count = 1
        if count > 9999 or count < 1:
            # TODO: send some funny troll message and if possible add some funny picture
            return

        real_price = self.calculate_item_price(count, custom_discount)

        if self.user_property_model.model_data.crystals < real_price: return
        if expected_price != False and not real_price == expected_price:
            # TODO: send some funny troll message and if possible add some funny picture
            return

        self.user_property_model.subtract_crystals(real_price)

        if self.item_model.user_owns_item:
            # we dont want to allow user to buy non countable item again
            if not self.game_object.model_class_exist(countable_item_model.CountableItemModel):
                return

            self.item_model.database_garage_item.count += count
            garage_tables.edit_item(self.item_model.database_garage_item, self.user_id)
        else:
            database_garage_item = self.client_object.database_garage_item_loader.create_new_database_garage_item(self.garage_item_object)
            database_garage_item.count = count
            garage_tables.add_item(database_garage_item, self.user_id) # add item to database
            self.item_model.database_garage_item = database_garage_item

            self.item_model.set_user_owns_to_true()
            self.item_model.mount_item()
