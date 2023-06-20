from client.dispatcher.dispatcher_model import model_data
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer
from . import weapon_weakening_model

class WeaponWeakeningModelData:
    def __init__(self, game_object, weapon_weakening_model_cc):
        self.game_object = game_object
        self.weapon_weakening_model_cc = weapon_weakening_model_cc

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.FloatCodec.encode(self.weapon_weakening_model_cc.maximum_damage_radius, buffer)
        basic_codecs.FloatCodec.encode(self.weapon_weakening_model_cc.minimum_damage_percent, buffer)
        basic_codecs.FloatCodec.encode(self.weapon_weakening_model_cc.minimum_damage_radius, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = self.game_object.get_model(weapon_weakening_model.WeaponWeakeningModel).model_id
        return _model_data
