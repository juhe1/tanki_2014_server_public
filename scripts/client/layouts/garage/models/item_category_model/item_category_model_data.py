from client.layouts.garage.models.item_category_model import item_category_model
from client.dispatcher.dispatcher_model import model_data
from client.layouts.garage import garage_codecs
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class ItemCategoryModelData:
    def __init__(self, game_object, client_object, garage_item_object):
        self.garage_item_object = garage_item_object
        self.game_object = game_object

        self.item_category_enum = garage_item_object.item_category

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        garage_codecs.ItemCategoryEnum.encode(self.item_category_enum, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = self.game_object.get_model(item_category_model.ItemCategoryModel).model_id
        return _model_data
