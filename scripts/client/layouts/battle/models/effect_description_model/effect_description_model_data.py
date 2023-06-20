from client.dispatcher.dispatcher_model import model_data
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer
from . import effect_description_model

class EffectDescriptionModelData:
    def __init__(self, effect_description_cc):
        self.effect_description_cc = effect_description_cc

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.IntCodec.encode(self.effect_description_cc.index, buffer)
        basic_codecs.BooleanCodec.encode(self.effect_description_cc.inventory, buffer)
        basic_codecs.LongCodec.encode(self.effect_description_cc.tank_game_object_id, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = effect_description_model.EffectDescriptionModel.model_id
        return _model_data
