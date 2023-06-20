from client.layouts.garage.models.buyable_model import buyable_model
from client.layouts.garage.models.garage_model import garage_model
from client.layouts.garage.models.item_model import item_model
from client.dispatcher.dispatcher_model import model_data
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class BuyableModelData:
    def __init__(self, game_object, client_object, garage_item_object, space, buyable_model):
        self.garage_item_object = garage_item_object
        self.game_object = game_object
        self.buyable_model = buyable_model
        self.garage_model = space.get_model(garage_model.GarageModel, "default_game_object")
        self.item_model = game_object.get_model(item_model.ItemModel)

        self.buyable = True # now this is always true because i dont see any use for the false
        self.price_without_discount = garage_item_object.price
        self.price_with_discount = garage_item_object.price - (garage_item_object.price * garage_item_object.discount)

    def calculate_kit_price(self):
        discount = self.garage_item_object.kit_discount
        price = 0

        for kit_item in self.garage_item_object.kit_items:
            item_game_object = self.garage_model.get_item_game_object_by_item_id(kit_item.item)
            item_item_model = item_game_object.get_model(item_model.ItemModel)
            item_buyable_model = item_game_object.get_model(buyable_model.BuyableModel)

            price += item_buyable_model.calculate_item_price(kit_item.count, discount)

        return int(price)

    def get_model_data(self):
        price = self.price_without_discount

        if self.garage_item_object.item_category == "kit":
            price = self.calculate_kit_price()

        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.BooleanCodec.encode(self.buyable, buffer)
        basic_codecs.IntCodec.encode(price, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = self.game_object.get_model(buyable_model.BuyableModel).model_id
        return _model_data
