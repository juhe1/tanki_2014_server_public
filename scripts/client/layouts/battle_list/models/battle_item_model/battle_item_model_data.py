from client.layouts.battle_list.models.battle_create_model import battle_create_model
from client.layouts.battle_list.models.battle_item_model import battle_item_model
from client.layouts.battle_list import battle_list_codecs
from client.dispatcher.dispatcher_model import model_data
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class BattleItemModelData:
    def __init__(self, game_object, battle_item_model_cc):
        self.game_object = game_object
        self.battle_item_model_cc = battle_item_model_cc

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.battle_item_model_cc.battle_id, buffer)
        battle_list_codecs.BattleModeCodec.encode(self.battle_item_model_cc.battle_mode, buffer)
        basic_codecs.LongCodec.encode(self.battle_item_model_cc.map_game_object_id, buffer)
        basic_codecs.ByteCodec.encode(self.battle_item_model_cc.max_people_count, buffer)
        basic_codecs.StringCodec.encode(self.battle_item_model_cc.name, buffer)
        basic_codecs.BooleanCodec.encode(self.battle_item_model_cc.without_supplies, buffer)
        basic_codecs.BooleanCodec.encode(self.battle_item_model_cc.private_battle, buffer)
        basic_codecs.BooleanCodec.encode(self.battle_item_model_cc.pro_battle, buffer)
        basic_codecs.RangeCodec.encode(self.battle_item_model_cc.rank_range, buffer)
        basic_codecs.BooleanCodec.encode(self.battle_item_model_cc.suspicious, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = self.game_object.get_model(battle_item_model.BattleItemModel).model_id
        return _model_data
