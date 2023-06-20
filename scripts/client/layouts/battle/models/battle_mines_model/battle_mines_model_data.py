from loaders.client_resource_loader import client_resource_loader
from client.dispatcher.dispatcher_model import model_data
from client.layouts.battle import battle_codecs
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer
from . import battle_mines_model
import server_properties

class BattleMinesModelData:
    def __init__(self, battle_mines_model_cc):
        self.battle_mines_model_cc = battle_mines_model_cc

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.battle_mines_model_cc.activate_sound, buffer)
        basic_codecs.IntCodec.encode(server_properties.MINE_ACTIVATE_TIME_MS, buffer)
        basic_codecs.VectorLevel1Codec.encode(self.battle_mines_model_cc.battle_mines, battle_codecs.BattleMineCodec, buffer)
        basic_codecs.LongCodec.encode(self.battle_mines_model_cc.blue_mine_texture, buffer)
        basic_codecs.LongCodec.encode(self.battle_mines_model_cc.deactivate_sound, buffer)
        basic_codecs.LongCodec.encode(self.battle_mines_model_cc.empty_mine_texture, buffer)
        basic_codecs.LongCodec.encode(self.battle_mines_model_cc.explosion_mark_texture, buffer)
        basic_codecs.LongCodec.encode(self.battle_mines_model_cc.explosion_sound, buffer)
        basic_codecs.FloatCodec.encode(server_properties.MINE_FAR_VISIBILITY_RADIUS, buffer)
        basic_codecs.LongCodec.encode(self.battle_mines_model_cc.friendly_mine_texture, buffer)
        basic_codecs.LongCodec.encode(self.battle_mines_model_cc.idle_explosion_texture, buffer)
        basic_codecs.FloatCodec.encode(server_properties.MINE_IMPACT_FORCE, buffer)
        basic_codecs.LongCodec.encode(self.battle_mines_model_cc.main_explosion_texture, buffer)
        basic_codecs.FloatCodec.encode(server_properties.MINE_MIN_DISTANCE_FROM_BASE, buffer)
        basic_codecs.LongCodec.encode(self.battle_mines_model_cc.model3ds, buffer)
        basic_codecs.FloatCodec.encode(server_properties.MINE_NEAR_VISIBLITY_RADIUS, buffer)
        basic_codecs.FloatCodec.encode(server_properties.MINE_RADIUS, buffer)
        basic_codecs.LongCodec.encode(self.battle_mines_model_cc.red_mine_texture, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = battle_mines_model.BattleMinesModel.model_id
        return _model_data
