from client.layouts.battle.models.inventory_item_model import first_aid_inventory_item_model
from client.layouts.battle.models.inventory_item_model import double_armor_inventory_item_model
from client.layouts.battle.models.inventory_item_model import double_power_inventory_item_model
from client.layouts.battle.models.inventory_item_model import nitro_inventory_item_model
from client.layouts.battle.models.inventory_item_model import mine_inventory_item_model
from client.space import game_object
from client.space.model import Model
from database import garage_tables
import server_properties

class InventoryModel(Model):
    model_id = 300100052

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.inventory_item_models = []

    def reset_timers(self):
        for _inventory_item_model in self.inventory_item_models:
            _inventory_item_model.supplie_timer.set_done()

    def loaded_from_client(self):
        self.init_inventory_items()

    def create_inventory_item_game_object(self, model, index):
        inventory_item_object = self.client_space.add_game_object(game_object_name="inventory_item")
        _inventory_item_model = inventory_item_object.add_model(model, model_args=(index,))
        inventory_item_object.load_object_from_client()

        self.inventory_item_models.append(_inventory_item_model)
        return inventory_item_object

    def init_inventory_items(self):
        self.create_inventory_item_game_object(first_aid_inventory_item_model.FirstAidInventoryItemModel, index=1)
        self.create_inventory_item_game_object(double_armor_inventory_item_model.DoubleArmorInventoryItemModel, index=2)
        self.create_inventory_item_game_object(double_power_inventory_item_model.DoublePowerInventoryItemModel, index=3)
        self.create_inventory_item_game_object(nitro_inventory_item_model.NitroInventoryItemModel, index=4)
        self.create_inventory_item_game_object(mine_inventory_item_model.MineInventoryItemModel, index=5)
