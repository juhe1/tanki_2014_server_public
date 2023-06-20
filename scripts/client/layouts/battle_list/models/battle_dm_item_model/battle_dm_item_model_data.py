from client.layouts.battle_list.models.battle_dm_item_model import battle_dm_item_model
from client.layouts.lobby.models.user_property_model import user_property_model
from client.dispatcher.dispatcher_model import model_data
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class BattleDmItemModelData:
    def __init__(self, client_object, game_object, battle_dm_item_model_cc):
        self.game_object = game_object
        self.user_ids = battle_dm_item_model_cc.user_ids
        self.delete_place_holder(client_object.user_id)

    def delete_place_holder(self, user_id):
        if user_id in self.user_ids:
            self.user_ids = self.user_ids.copy()
            self.user_ids.remove(user_id)

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.VectorLevel1Codec.encode(self.user_ids, basic_codecs.LongCodec, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = self.game_object.get_model(battle_dm_item_model.BattleDmItemModel).model_id
        return _model_data
