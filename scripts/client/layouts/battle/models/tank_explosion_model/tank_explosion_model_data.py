from loaders.client_resource_loader import client_resource_loader
from client.dispatcher.dispatcher_model import model_data
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer
from . import tank_explosion_model

class TankExplosionModelData:
    def __init__(self, game_object, tank_explosion_model_cc):
        self.game_object = game_object
        self.tank_explosion_model_cc = tank_explosion_model_cc

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.tank_explosion_model_cc.explosion_texture, buffer)
        basic_codecs.LongCodec.encode(self.tank_explosion_model_cc.shock_wave_texture, buffer)
        basic_codecs.LongCodec.encode(self.tank_explosion_model_cc.smoke_texture, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = self.game_object.get_model(tank_explosion_model.TankExplosionModel).model_id
        return _model_data
