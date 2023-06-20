from client.dispatcher.dispatcher_model import model_data
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer
from . import weapon_common_model

class WeaponCommonModelData:
    def __init__(self, game_object, weapon_common_model_cc):
        self.game_object = game_object
        self.weapon_common_model_cc = weapon_common_model_cc

        if weapon_common_model_cc.kickback is None:
            weapon_common_model_cc.kickback = 0

        if weapon_common_model_cc.impact_force is None:
            weapon_common_model_cc.impact_force = 0

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.FloatCodec.encode(self.weapon_common_model_cc.impact_force, buffer)
        basic_codecs.FloatCodec.encode(self.weapon_common_model_cc.kickback, buffer)
        basic_codecs.FloatCodec.encode(self.weapon_common_model_cc.turret_rotation_acceleration, buffer)
        basic_codecs.FloatCodec.encode(self.weapon_common_model_cc.turret_rotation_speed, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = self.game_object.get_model(weapon_common_model.WeaponCommonModel).model_id
        return _model_data
