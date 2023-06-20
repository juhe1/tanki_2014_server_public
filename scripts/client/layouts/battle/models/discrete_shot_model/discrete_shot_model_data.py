from client.dispatcher.dispatcher_model import model_data
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer
from . import discrete_shot_model

class DiscreteShotModelData:
    def __init__(self, game_object, discrete_shot_model_cc):
        self.game_object = game_object
        self.discrete_shot_model_cc = discrete_shot_model_cc

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.FloatCodec.encode(self.discrete_shot_model_cc.auto_aiming_angle_down, buffer)
        basic_codecs.FloatCodec.encode(self.discrete_shot_model_cc.auto_aiming_angle_up, buffer)
        basic_codecs.FloatCodec.encode(self.discrete_shot_model_cc.reload_msec, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = self.game_object.get_model(discrete_shot_model.DiscreteShotModel).model_id
        return _model_data
