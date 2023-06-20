from client.dispatcher.dispatcher_model import model_data
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer
from . import inventory_item_model
import server_properties

class InventoryItemModelData:
    def __init__(self, count, index, cool_down_time_in_sec, battle_game_object_id):
        self.battle_game_object_id = battle_game_object_id
        self.cool_down_time_in_sec = cool_down_time_in_sec
        self.count = count
        self.item_index = index

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.battle_game_object_id, buffer)
        basic_codecs.IntCodec.encode(self.cool_down_time_in_sec, buffer)
        basic_codecs.IntCodec.encode(self.count, buffer)
        basic_codecs.IntCodec.encode(self.item_index, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = inventory_item_model.InventoryItemModel.model_id
        return _model_data
