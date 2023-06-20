from client.dispatcher.dispatcher_model import model_data
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer
from . import bonus_common_model

class BonusCommonModelData:
    def __init__(self, bonus_common_cc):
        self.bonus_common_cc = bonus_common_cc

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()

        basic_codecs.LongCodec.encode(self.bonus_common_cc.box_resource, buffer)
        basic_codecs.LongCodec.encode(self.bonus_common_cc.cord_resource, buffer)
        basic_codecs.IntCodec.encode(self.bonus_common_cc.life_time, buffer)
        basic_codecs.LongCodec.encode(self.bonus_common_cc.parachute_inner_resource, buffer)
        basic_codecs.LongCodec.encode(self.bonus_common_cc.parachute_resource, buffer)
        basic_codecs.LongCodec.encode(self.bonus_common_cc.pickup_sound_resource, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = bonus_common_model.BonusCommonModel.model_id
        return _model_data
