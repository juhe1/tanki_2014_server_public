from client.layouts.garage.models.buyable_model import buyable_model
from client.layouts.garage import garage_codecs
from utils.binary.codecs import basic_codecs

class UpgradeGarageItemModelCommandHandler:
    def __init__(self, client_object):
        self.client_object = client_object

        self.UPGRADE_ITEM_COMMAND_ID = 300040013
        self.SPEED_UP_COMMAND_ID = 300040012
        self.INSTANT_UPGRADE_COMMAND_ID = 300040011

    def handle_command(self, binary_data, command_id):
        if command_id == self.UPGRADE_ITEM_COMMAND_ID:
            self.upgrade_item(binary_data)
            return True
        if command_id == self.SPEED_UP_COMMAND_ID:
            self.speed_up(binary_data)
            return True
        if command_id == self.INSTANT_UPGRADE_COMMAND_ID:
            self.instant_upgrade(binary_data)
            return True
        return False

    def instant_upgrade(self, binary_data):
        item_game_object_id = basic_codecs.LongCodec.decode(binary_data)
        property_id = basic_codecs.IntCodec.decode(binary_data)
        num_levels = basic_codecs.IntCodec.decode(binary_data)
        expected_price = basic_codecs.IntCodec.decode(binary_data)

        item_buyable_model = self.client_object.client_space_registry.get_model(space_name="garage", game_object_id=item_game_object_id, model=buyable_model.BuyableModel)
        if item_buyable_model == None: return
        item_buyable_model.instant_upgrade(property_id, num_levels, expected_price)

    def upgrade_item(self, binary_data):
        item_game_object_id = basic_codecs.LongCodec.decode(binary_data)
        property_id = basic_codecs.IntCodec.decode(binary_data)
        expected_price = basic_codecs.IntCodec.decode(binary_data)
        expected_time_in_seconds = basic_codecs.IntCodec.decode(binary_data)

        item_buyable_model = self.client_object.client_space_registry.get_model(space_name="garage", game_object_id=item_game_object_id, model=buyable_model.BuyableModel)
        if item_buyable_model == None: return
        item_buyable_model.upgrade_item(property_id, expected_price, expected_time_in_seconds)

    def speed_up(self, binary_data):
        item_game_object_id = basic_codecs.LongCodec.decode(binary_data)
        expected_price = basic_codecs.IntCodec.decode(binary_data)

        item_buyable_model = self.client_object.client_space_registry.get_model(space_name="garage", game_object_id=item_game_object_id, model=buyable_model.BuyableModel)
        if item_buyable_model == None: return
        item_buyable_model.buy_speed_up(expected_price)
