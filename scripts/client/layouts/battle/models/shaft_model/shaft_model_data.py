from client.dispatcher.dispatcher_model import model_data
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer
from . import shaft_model

class ShaftModelData:
    def __init__(self, shaft_model_cc):
        self.shaft_model_cc = shaft_model_cc

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.IntCodec.encode(self.shaft_model_cc.after_shot_pause, buffer)
        basic_codecs.FloatCodec.encode(self.shaft_model_cc.aiming_impact, buffer)
        basic_codecs.FloatCodec.encode(self.shaft_model_cc.charge_rate, buffer)
        basic_codecs.FloatCodec.encode(self.shaft_model_cc.discharge_rate, buffer)
        basic_codecs.FloatCodec.encode(self.shaft_model_cc.fast_shot_energy, buffer)
        basic_codecs.FloatCodec.encode(self.shaft_model_cc.horizontal_targeting_speed, buffer)
        basic_codecs.FloatCodec.encode(self.shaft_model_cc.initial_fov, buffer)
        basic_codecs.FloatCodec.encode(self.shaft_model_cc.jitter_angle_max, buffer)
        basic_codecs.FloatCodec.encode(self.shaft_model_cc.jitter_angle_min, buffer)
        basic_codecs.FloatCodec.encode(self.shaft_model_cc.jitter_intencity_max, buffer)
        basic_codecs.FloatCodec.encode(self.shaft_model_cc.jitter_intencity_min, buffer)
        basic_codecs.FloatCodec.encode(self.shaft_model_cc.jitter_start_point, buffer)
        basic_codecs.FloatCodec.encode(self.shaft_model_cc.max_energy, buffer)
        basic_codecs.FloatCodec.encode(self.shaft_model_cc.minimum_fov, buffer)
        basic_codecs.LongCodec.encode(self.shaft_model_cc.reticle_image, buffer)
        basic_codecs.FloatCodec.encode(self.shaft_model_cc.rotation_coeff_kmin, buffer)
        basic_codecs.FloatCodec.encode(self.shaft_model_cc.rotation_coeff_T1, buffer)
        basic_codecs.FloatCodec.encode(self.shaft_model_cc.rotation_coeff_T2, buffer)
        basic_codecs.FloatCodec.encode(self.shaft_model_cc.shrubs_hiding_radius_max, buffer)
        basic_codecs.FloatCodec.encode(self.shaft_model_cc.shrubs_hiding_radius_min, buffer)
        basic_codecs.FloatCodec.encode(self.shaft_model_cc.targeting_acceleration, buffer)
        basic_codecs.IntCodec.encode(self.shaft_model_cc.targeting_transition_time, buffer)
        basic_codecs.FloatCodec.encode(self.shaft_model_cc.vertical_targeting_speed, buffer)
        basic_codecs.FloatCodec.encode(self.shaft_model_cc.weakening_coeff, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = shaft_model.ShaftModel.model_id
        return _model_data
