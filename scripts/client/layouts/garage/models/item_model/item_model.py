from client.layouts.garage.models.upgradeable_params_constructor_model import upgradeable_params_constructor_model
from client.layouts.garage.models.discount_for_upgrade_model import discount_for_upgrade_model
from client.layouts.garage.models.countable_item_model import countable_item_model
from client.layouts.garage.models.temporary_item_model import temporary_item_model
from client.layouts.garage.models.item_category_model import item_category_model
from client.layouts.lobby.models.user_property_model import user_property_model
from client.layouts.garage.models.modification_model import modification_model
from client.layouts.garage.models.description_model import description_model
from client.layouts.garage.models.object_3ds_model import object_3ds_model
from client.layouts.garage.models.data_owner_model import data_owner_model
from client.layouts.garage.models.garage_kit_model import garage_kit_model
from client.layouts.garage.models.coloring_model import coloring_model
from client.layouts.garage.models.discount_model import discount_model
from client.layouts.garage.codec_data_structs import garage_item_info
from client.layouts.garage.models.item_3d_model import item_3d_model
from client.layouts.garage.models.buyable_model import buyable_model
from client.layouts.garage.models.item_model import item_model_data
from client.layouts.garage.models.garage_model import garage_model
from loaders.garage_item_loader import garage_item_loader
from client.space.model import Model
from database import garage_tables
from utils import list_utils

class ItemModel(Model):
    model_id = 300040012

    def __init__(self, game_object, client_space, client_object, garage_item_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.model_data = item_model_data.ItemModelData(game_object, client_object, garage_item_object)
        self.commands = None
        self.command_handler = None

        self.item_id = garage_item_object.id
        self.garage_item_object = garage_item_object
        self.garage_model = client_space.get_model(game_object_name="default_game_object", model=garage_model.GarageModel)

        self.database_garage_item = self.client_object.database_garage_item_loader.get_item_by_id(self.garage_item_object.id) # get all item data that is stored in database
        self.user_owns_item = False
        self.mounted = False
        self.garage_item_info_object = None

        # user own the item if there is some data of the item in the database
        if self.database_garage_item:
            self.user_owns_item = True

    def init_done(self):
        self.create_models_for_item()
        self.add_item_to_list()

    def unload_item(self):
        # unload item game object from client and from server
        self.client_space.get_game_object_by_id(self.game_object.id).remove_game_object()

    def mount_item(self):
        self.game_object.load_models_from_client([item_3d_model.Item3DModel]) # this is temporary solution. i will change it when i figure out how it should be done

        # try mount item from database and if we fail return
        if garage_tables.mount_item(self.database_garage_item, self.garage_item_object.item_category, self.client_object.user_id) == False:
            return

        self.garage_model.mount_item(self.game_object.id, self.garage_item_object.item_category)

    def get_next_modification_game_object(self):
        next_mod_id = self.garage_item_object.modification_index + 1
        next_modification_garage_item = garage_item_loader.get_item_by_base_id_and_mod_idx(self.garage_item_object.base_item_id, next_mod_id)
        next_modification_game_object = self.garage_model.get_item_game_object_by_item_id(next_modification_garage_item.id)
        return next_modification_game_object

    def set_user_owns_to_true(self):
        self.user_owns_item = True
        self.database_garage_item = self.client_object.database_garage_item_loader.get_item_by_id(self.garage_item_object.id)

    def set_user_owns_to_false(self):
        self.user_owns_item = False
        garage_tables.remove_item(self.database_garage_item, self.client_object.user_id)

    # this function determines where to put the item. so we put it to garage_items or mounted_items or market_items
    def add_item_to_list(self):
        mounted_items = self.client_object.database_garage_item_loader.get_mounted_items()
        if self.garage_item_object.id in mounted_items.values():
            self.garage_model.mount_item(self.game_object.id, self.garage_item_object.item_category)

        if self.user_owns_item:
            self.garage_model.depot_items.append(self.game_object.id)
            return

        if self.garage_item_object.modification_index != None:
            if self.garage_item_object.modification_index == 0: # if item is m0 add it to shop
                self.garage_model.market_items.append(self.game_object.id)
            return
        else: # if item is not moddable then add it to shop
            self.garage_model.market_items.append(self.game_object.id)

    # this function find out what models need to be loaded and then it also loads them
    def create_models_for_item(self):
        self.game_object.add_model(description_model.DescriptionModel, model_args=(self.garage_item_object,))
        self.game_object.add_model(item_category_model.ItemCategoryModel, model_args=(self.garage_item_object,))

        if self.garage_item_object.data_owner_id:
            self.game_object.add_model(data_owner_model.DataOwnerModel, model_args=(self.garage_item_object.data_owner_id,))

        if self.garage_item_object.price:
            self.game_object.add_model(buyable_model.BuyableModel, model_args=(self.garage_item_object,))

        if self.garage_item_object.discount != None:
            self.game_object.add_model(discount_model.DiscountModel, model_args=(self.garage_item_object,))

        if self.garage_item_object.modification_index != None:
            self.game_object.add_model(modification_model.ModificationModel, model_args=(self.garage_item_object,))

        if self.garage_item_object.object_3ds != None:
            self.game_object.add_model(item_3d_model.Item3DModel)
            self.game_object.add_model(object_3ds_model.Object3DSModel, model_args=(self.garage_item_object.object_3ds,))

        if self.garage_item_object.coloring != None:
            self.game_object.add_model(item_3d_model.Item3DModel)
            self.game_object.add_model(coloring_model.ColoringModel, model_args=(self.garage_item_object.coloring,))

        if self.garage_item_object.count != None:
            self.game_object.add_model(countable_item_model.CountableItemModel, model_args=(self.garage_item_object,))

        if self.garage_item_object.kit_items:
            self.game_object.add_model(garage_kit_model.GarageKitModel, model_args=(self.garage_item_object,))

        if self.garage_item_object.temporary_item_life_time_in_sec:
            self.game_object.add_model(temporary_item_model.TemporaryItemModel, model_args=(self.garage_item_object,))

        if self.garage_item_object.upgradable_property_datas != []:
            self.game_object.add_model(discount_for_upgrade_model.DiscountForUpgradeModel, model_args=(self.garage_item_object,))
            self.game_object.add_model(upgradeable_params_constructor_model.UpgradeableParamsConstructorModel, model_args=(self.garage_item_object,))
