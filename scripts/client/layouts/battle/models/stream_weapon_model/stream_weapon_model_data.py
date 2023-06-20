from client.dispatcher.dispatcher_model import model_data
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer
from . import stream_weapon_model

class StreamWeaponModelData:
    def __init__(self, stream_weapon_model_cc):
        self.stream_weapon_model_cc = stream_weapon_model_cc

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.FloatCodec.encode(self.stream_weapon_model_cc.energy_capacity, buffer)
        basic_codecs.FloatCodec.encode(self.stream_weapon_model_cc.energy_discharge_speed, buffer)
        basic_codecs.FloatCodec.encode(self.stream_weapon_model_cc.energy_recharge_speed, buffer)
        basic_codecs.FloatCodec.encode(self.stream_weapon_model_cc.weapon_tick_interval_msec, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = stream_weapon_model.StreamWeaponModel.model_id
        return _model_data
