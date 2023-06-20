from client.layouts.garage.models.countable_item_model import countable_item_model
from client.layouts.garage.models.item_model import item_model
from client.dispatcher.dispatcher_model import model_data
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class CountableItemModelData:
    def __init__(self, game_object, client_object, garage_item_object):
        self.garage_item_object = garage_item_object
        self.game_object = game_object
        self.item_model = game_object.get_model(item_model.ItemModel)
        self.database_garage_item = self.item_model.database_garage_item

        self.count = 0
        if self.database_garage_item != None:
            self.count = self.database_garage_item.count

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.IntCodec.encode(self.count, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = self.game_object.get_model(countable_item_model.CountableItemModel).model_id
        return _model_data
