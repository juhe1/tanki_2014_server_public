from client.layouts.battle_list.models.pro_battle_info_model import pro_battle_info_model
from client.layouts.garage.models.garage_model import garage_model
from client.dispatcher.dispatcher_model import model_data
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer
from database import garage_tables
import server_properties

import datetime

class ProBattleInfoModelData:
    def __init__(self, game_object, client_object):
        self.game_object = game_object

        self.pro_battle_enter_price = server_properties.PRO_BATTLE_ENTER_PRICE
        self.battle_pass_time_left_in_sec = self.get_pro_pass_time_left(client_object)

    def get_pro_pass_time_left(self, client_object):
        battle_pass_database_garage_item = client_object.database_garage_item_loader.get_item_by_id(800)
        if battle_pass_database_garage_item != None:
            expiration_time = battle_pass_database_garage_item.temporary_item_expiration_time
            time_now = datetime.datetime.now()
            time_left = (expiration_time - time_now).seconds
            if time_left < 1:
                time_left = 0
        else:
            time_left = 0
        return time_left

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.IntCodec.encode(self.pro_battle_enter_price, buffer)
        basic_codecs.IntCodec.encode(self.battle_pass_time_left_in_sec, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = self.game_object.get_model(pro_battle_info_model.ProBattleInfoModel).model_id
        return _model_data
