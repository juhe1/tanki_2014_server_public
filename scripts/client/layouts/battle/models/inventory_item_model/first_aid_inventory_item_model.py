from . import inventory_item_model
from loaders.server_properties_loader import server_properties_loader

class FirstAidInventoryItemModel(inventory_item_model.InventoryItemModel):

    def __init__(self, game_object, client_space, client_object, index, global_model=None):
        cool_down_time_in_sec = server_properties_loader.properties.first_aid_cool_down_time_in_sec
        item_id = server_properties_loader.properties.first_aid_item_id

        super().__init__(game_object, client_space, client_object, item_id, index, cool_down_time_in_sec, global_model)

    def activate_effect(self):
        self.tank_global_game_object.activate_first_aid_effect()
