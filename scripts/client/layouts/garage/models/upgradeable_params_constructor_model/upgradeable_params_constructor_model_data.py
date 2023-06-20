from client.layouts.garage.models.upgradeable_params_constructor_model import upgradeable_params_constructor_model
from client.layouts.garage.codec_data_structs import upgrading_property_info
from client.layouts.garage.models.garage_model import garage_model
from client.layouts.garage.models.item_model import item_model
from client.dispatcher.dispatcher_model import model_data
from client.layouts.garage import garage_codecs
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer
from database import garage_tables

import datetime
import copy

class UpgradeableParamsConstructorModelData:
    def __init__(self, game_object, client_object, garage_item_object, _upgradeable_params_constructor_model):
        self.garage_item_object = garage_item_object
        self.game_object = game_object
        self.upgradeable_params_constructor_model = _upgradeable_params_constructor_model

        self.item_model = game_object.get_model(item_model.ItemModel)
        self.database_garage_item = self.item_model.database_garage_item
        client_space = self.item_model.client_space
        self.garage_model = client_space.get_model(garage_model.GarageModel, "default_game_object")

        self.info = self.get_info()
        self.upgradable_properties = garage_item_object.upgradable_property_datas

    def get_info(self):
        if self.database_garage_item == None or self.database_garage_item.upgrade_done_time == None:
            return

        done_time = self.database_garage_item.upgrade_done_time
        datetime_now = datetime.datetime.now()

        upgrading_property_id = self.database_garage_item.upgrading_property_id
        upgrading_property_data = self.garage_item_object.get_upgradable_property_data_by_id(upgrading_property_id)

        info = upgrading_property_info.UpgradingPropertyInfo()
        info.remaining_time_in_ms = (done_time - datetime_now).seconds * 1000
        info.property_id = upgrading_property_data.property_id
        return info

    def get_model_data(self):
        if self.item_model.user_owns_item:
            new_upgradable_propertys = []
            # add properties to every upgradable_property
            for upgradable_property in self.upgradable_properties:
                upgradable_property_copy = copy.deepcopy(upgradable_property) # we make copy of this object, because we want to add some client specifig stuff to it
                upgradable_property_copy.properties = self.garage_item_object.properties

                # get from database garage_property levels and set them to the item
                property_id = upgradable_property_copy.property_id
                upgradable_property_copy.level = self.item_model.database_garage_item.upgradable_property_data_levels[property_id]

                new_upgradable_propertys.append(upgradable_property_copy)
        else:
            new_upgradable_propertys = self.upgradable_properties

        # write data to buffer
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.OptionalCodec.encode((self.info, buffer), buffer, garage_codecs.UpgradingPropertyInfo)
        basic_codecs.VectorLevel1Codec.encode(new_upgradable_propertys, garage_codecs.GaragePropertyData, buffer)

        # create model_data object
        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = self.game_object.get_model(upgradeable_params_constructor_model.UpgradeableParamsConstructorModel).model_id
        return _model_data
