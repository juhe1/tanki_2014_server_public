from . import inventory_item_model
import server_properties

class DoubleArmorInventoryItemModel(inventory_item_model.InventoryItemModel):

    def __init__(self, game_object, client_space, client_object, index, global_model=None):
        cool_down_time_in_sec = server_properties.DOUBLE_ARMOR_COOL_DOWN_TIME_IN_SEC
        item_id = server_properties.DOUBLE_ARMOR_ITEM_ID

        super().__init__(game_object, client_space, client_object, item_id, index, cool_down_time_in_sec, global_model)

    def activate_effect(self):
        self.tank_global_game_object.activate_double_armor_effect()
