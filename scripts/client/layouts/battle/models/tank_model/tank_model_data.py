from client.layouts.battle.models.tank_model import tank_model
from client.dispatcher.dispatcher_model import model_data
from client.layouts.battle import battle_codecs
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class TankModelData:
    def __init__(self, game_object, tank_model_cc, local):
        self.game_object = game_object
        self.tank_model_cc = tank_model_cc
        self.local = local

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.FloatCodec.encode(self.tank_model_cc.damping, buffer)
        basic_codecs.BooleanCodec.encode(self.local, buffer)
        basic_codecs.FloatCodec.encode(self.tank_model_cc.mass, buffer)
        basic_codecs.IntCodec.encode(self.tank_model_cc.max_health, buffer)
        battle_codecs.TankSoundsCodec.encode(self.tank_model_cc.sounds, buffer)
        battle_codecs.TankInitializationDataCodec.encode(self.tank_model_cc.tank_initialization_data, buffer)
        battle_codecs.TankPartsCodec.encode(self.tank_model_cc.tank_parts, buffer)
        battle_codecs.TankResourcesCodec.encode(self.tank_model_cc.tank_resources, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = self.game_object.get_model(tank_model.TankModel).model_id
        return _model_data
