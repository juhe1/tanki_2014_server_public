from loaders.server_properties_loader import server_properties_loader
from client.layouts.garage.models.upgrade_garage_item_model import upgrade_garage_item_model
from client.dispatcher.dispatcher_model import model_data
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class UpgradeGarageItemModelData:
    def __init__(self, game_object, client_object):
        self.game_object = game_object

        self.enable_upgrades = server_properties_loader.properties.enable_upgrades
        self.upgrade_speedup_coefficient = server_properties_loader.properties.upgrade_speedup_coefficient

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.BooleanCodec.encode(self.enable_upgrades, buffer)
        basic_codecs.FloatCodec.encode(self.upgrade_speedup_coefficient, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = self.game_object.get_model(upgrade_garage_item_model.UpgradeGarageItemModel).model_id
        return _model_data
