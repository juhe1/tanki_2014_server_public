from client.layouts.battle_list.models.map_info_model import map_info_model
from loaders.client_resource_loader import client_resource_loader
from client.dispatcher.dispatcher_model import model_data
from client.layouts.battle_list import battle_list_codecs
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class MapInfoModelData:
    def __init__(self, game_object, client_object, map_info_model_cc):
        self.game_object = game_object
        self.map_info_model_cc = map_info_model_cc

        if client_object.language == "en":
            self.map_name = map_info_model_cc.name_en

        if client_object.language == "ru":
            self.map_name = map_info_model_cc.name_ru

        self.map_info_model_cc.enabled = True

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.BooleanCodec.encode(self.map_info_model_cc.enabled, buffer)
        basic_codecs.LongCodec.encode(self.map_info_model_cc.map_id, buffer)
        basic_codecs.StringCodec.encode(self.map_name, buffer)
        basic_codecs.ShortCodec.encode(self.map_info_model_cc.max_people, buffer)
        basic_codecs.LongCodec.encode(self.map_info_model_cc.preview_image, buffer)
        basic_codecs.RangeCodec.encode(self.map_info_model_cc.rank_limit, buffer)
        basic_codecs.VectorLevel1Codec.encode(self.map_info_model_cc.supported_modes, battle_list_codecs.BattleModeCodec, buffer)
        battle_list_codecs.MapThemeCodec.encode(self.map_info_model_cc.theme, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = self.game_object.get_model(map_info_model.MapInfoModel).model_id
        return _model_data
