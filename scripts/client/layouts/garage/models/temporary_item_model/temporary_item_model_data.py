from client.layouts.garage.models.temporary_item_model import temporary_item_model
from client.layouts.lobby.models.user_property_model import user_property_model
from client.layouts.garage.models.item_model import item_model
from client.dispatcher.dispatcher_model import model_data
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer
from database import garage_tables


import datetime

class TemporaryItemModelData:
    def __init__(self, game_object, client_object, garage_item_object):
        self.garage_item_object = garage_item_object
        self.game_object = game_object
        self.item_model = game_object.get_model(item_model.ItemModel)
        self.database_garage_item = self.item_model.database_garage_item
        self.lobby_space = client_object.client_space_registry.get_space_by_name("lobby")

        self.life_time_in_sec = self.garage_item_object.temporary_item_life_time_in_sec
        self.remaining_time_in_sec = self.garage_item_object.temporary_item_remaining_time_in_sec

        if self.database_garage_item == None: return

        time_now = datetime.datetime.now()
        expiration_time = self.database_garage_item.temporary_item_expiration_time

        # delete temporary_item if it is expired
        if time_now > expiration_time:
            garage_tables.remove_item(self.database_garage_item, client_object.user_id)
            self.item_model.user_owns_item = False
        else:
            self.remaining_time_in_sec = (expiration_time - time_now).seconds


    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.IntCodec.encode(self.life_time_in_sec, buffer)
        basic_codecs.IntCodec.encode(self.remaining_time_in_sec, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = self.game_object.get_model(temporary_item_model.TemporaryItemModel).model_id
        return _model_data
