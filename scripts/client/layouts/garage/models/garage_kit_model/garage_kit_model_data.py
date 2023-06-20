from client.layouts.garage.models.garage_kit_model import garage_kit_model
from client.layouts.garage.models.garage_model import garage_model
from loaders.client_resource_loader import client_resource_loader
from client.dispatcher.dispatcher_model import model_data
from client.layouts.garage import garage_codecs
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

import copy

class GarageKitModelData:
    def __init__(self, game_object, client_object, garage_item_object):
        self.space = game_object.space
        self.garage_item_object = garage_item_object
        self.game_object = game_object
        self.garage_model = self.space.get_model(game_object_name="default_game_object", model=garage_model.GarageModel)

        #self.discount_items = garage_item_object.kit_discount_items
        self.image = client_resource_loader.get_resource_id(garage_item_object.kit_image)
        self.kit_items = garage_item_object.kit_items

    def get_model_data(self):
        kit_item_copies = []
        # we need to replace static item id to be item game object id
        for kit_item in self.garage_item_object.kit_items:
            kit_item_copy = copy.deepcopy(kit_item)
            kit_item_copy.item = self.garage_model.all_items[kit_item_copy.item].id
            kit_item_copies.append(kit_item_copy)

        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.VectorLevel1Codec.encode([], garage_codecs.DiscountItem, buffer)
        basic_codecs.LongCodec.encode(self.image, buffer)
        basic_codecs.VectorLevel1Codec.encode(kit_item_copies, garage_codecs.KitItem, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = self.game_object.get_model(garage_kit_model.GarageKitModel).model_id
        return _model_data
