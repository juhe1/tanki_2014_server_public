from client.layouts.garage.models.upgrade_garage_item_model import upgrade_garage_item_model
from client.dispatcher.dispatcher_model import model_data
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer
import server_properties

class UpgradeGarageItemModelData:
    def __init__(self, game_object, client_object):
        self.game_object = game_object

        self.enable_upgrades = server_properties.ENABLE_UPGRADES
        self.upgrade_speedup_coefficient = server_properties.UPGRADE_SPEEDUP_COEFFICIENT

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.BooleanCodec.encode(self.enable_upgrades, buffer)
        basic_codecs.FloatCodec.encode(self.upgrade_speedup_coefficient, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = self.game_object.get_model(upgrade_garage_item_model.UpgradeGarageItemModel).model_id
        return _model_data
