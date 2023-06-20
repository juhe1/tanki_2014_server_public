from client.layouts.battle_list.models.clan_info_model import clan_info_model
from client.dispatcher.dispatcher_model import model_data
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class ClanInfoModelData:
    def __init__(self, game_object, clan_info_model_cc):
        self.game_object = game_object
        self.clan_info_model_cc = clan_info_model_cc

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.StringCodec.encode(self.clan_info_model_cc.clan_link, buffer)
        basic_codecs.StringCodec.encode(self.clan_info_model_cc.clan_name, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = self.game_object.get_model(clan_info_model.ClanInfoModel).model_id
        return _model_data
