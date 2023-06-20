from client.layouts.battle.models.lighting_sfx_model import lighting_sfx_model
from client.dispatcher.dispatcher_model import model_data
from client.layouts.battle import battle_codecs
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class LightingSfxModelData:
    def __init__(self, game_object, lighting_sfx_model_cc):
        self.game_object = game_object
        self.lighting_effects = lighting_sfx_model_cc.lighting_effects

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.VectorLevel1Codec.encode(self.lighting_effects, battle_codecs.LightingEffectCodec, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = self.game_object.get_model(lighting_sfx_model.LightingSfxModel).model_id
        return _model_data
