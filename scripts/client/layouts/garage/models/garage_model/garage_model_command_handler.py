from client.layouts.garage.models.buyable_model import buyable_model
from client.layouts.garage.models.item_model import item_model
from utils.binary.codecs import basic_codecs

class GarageModelCommandHandler:
    def __init__(self, client_object):
        self.client_object = client_object

        self.ITEM_BOUGHT_COMMAND_ID = 300040000
        self.NEXT_MODIFICATION_BOUGHT_COMMAND_ID = 300040003
        self.KIT_BOUGHT_COMMAND_ID = 300040002
        self.ITEM_MOUNTED_COMMAND_ID = 300040001

    def handle_command(self, binary_data, command_id):
        if command_id == self.ITEM_BOUGHT_COMMAND_ID:
            self.item_bought(binary_data)
            return True
        if command_id == self.NEXT_MODIFICATION_BOUGHT_COMMAND_ID:
            self.next_modification_bought(binary_data)
            return True
        if command_id == self.KIT_BOUGHT_COMMAND_ID:
            self.kit_bought(binary_data)
            return True
        if command_id == self.ITEM_MOUNTED_COMMAND_ID:
            self.item_mounted(binary_data)
            return True
        return False

    def item_mounted(self, binary_data):
        item_game_object_id = basic_codecs.LongCodec.decode(binary_data)

        item_item_model = self.client_object.client_space_registry.get_model(space_name="garage", game_object_id=item_game_object_id, model=item_model.ItemModel)
        if item_item_model == None: return
        item_item_model.mount_item()

    def kit_bought(self, binary_data):
        item_game_object_id = basic_codecs.LongCodec.decode(binary_data)
        expected_price = basic_codecs.IntCodec.decode(binary_data)

        item_buyable_model = self.client_object.client_space_registry.get_model(space_name="garage", game_object_id=item_game_object_id, model=buyable_model.BuyableModel)
        if item_buyable_model == None: return # return if there is not such game_object or if the game_object doesnt have buyable_model
        item_buyable_model.kit_bought()

    def item_bought(self, binary_data):
        item_game_object_id = basic_codecs.LongCodec.decode(binary_data)
        count = basic_codecs.IntCodec.decode(binary_data)
        expected_price = basic_codecs.IntCodec.decode(binary_data)

        item_buyable_model = self.client_object.client_space_registry.get_model(space_name="garage", game_object_id=item_game_object_id, model=buyable_model.BuyableModel)
        if item_buyable_model == None: return # return if there is not such game_object or if the game_object doesnt have buyable_model
        item_buyable_model.item_bought(count, expected_price=expected_price)

    def next_modification_bought(self, binary_data):
        item_game_object_id = basic_codecs.LongCodec.decode(binary_data)
        expected_price = basic_codecs.IntCodec.decode(binary_data)

        item_buyable_model = self.client_object.client_space_registry.get_model(space_name="garage", game_object_id=item_game_object_id, model=buyable_model.BuyableModel)
        if item_buyable_model == None: return # return if there is not such game_object or if the game_object doesnt have buyable_model
        item_buyable_model.buy_next_modification()
