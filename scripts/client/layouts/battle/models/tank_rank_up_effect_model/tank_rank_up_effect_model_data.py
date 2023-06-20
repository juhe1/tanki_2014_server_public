from loaders.client_resource_loader import client_resource_loader
from client.dispatcher.dispatcher_model import model_data
from utils.binary.codecs import basic_codecs
from . import tank_rank_up_effect_model
from utils.binary import binary_buffer

class TankRankUpEffectModelData:
    def __init__(self, game_object, tank_rank_up_effect_model_cc):
        self.game_object = game_object
        self.rank_up_sound = tank_rank_up_effect_model_cc.rank_up_sound

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.rank_up_sound, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = self.game_object.get_model(tank_rank_up_effect_model.TankRankUpEffectModel).model_id
        return _model_data
