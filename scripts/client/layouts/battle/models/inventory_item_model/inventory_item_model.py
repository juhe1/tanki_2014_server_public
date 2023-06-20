from client.layouts.battle.models.battle_field_model import battle_field_model
from client.layouts.battle.models.tank_model import tank_model
from . import inventory_item_model_command_handler
from . import inventory_item_model_commands
from . import inventory_item_model_data
from client.space.model import Model
from utils.time.timer import Timer
from database import garage_tables

class InventoryItemModel(Model):
    model_id = 300100051

    def __init__(self, game_object, client_space, client_object, item_id, index, cool_down_time_in_sec, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.tank_global_game_object = client_space.get_model(tank_model.TankModel, game_object_id=client_object.user_id).global_model # this will be used in sub classes
        self.database_garage_item = self.client_object.database_garage_item_loader.get_item_by_id(item_id)

        self.supplie_timer = Timer(cool_down_time_in_sec)
        self.supplie_timer.set_done()

        battle_game_object_id = client_space.get_game_object_by_name("default_game_object").id
        count = self.get_supplie_count()

        self.model_data = inventory_item_model_data.InventoryItemModelData(count, index, cool_down_time_in_sec, battle_game_object_id)
        self.commands = inventory_item_model_commands.InventoryItemModelCommands(client_space, game_object)
        self.command_handler = inventory_item_model_command_handler.InventoryItemModelCommandHandler(self)

    def get_supplie_count(self):
        if self.database_garage_item == None: return 0
        return self.database_garage_item.count

    def subtract_supplie_from_user(self):
        self.database_garage_item.count -= 1
        garage_tables.edit_item(self.database_garage_item, self.client_object.user_id)

    def try_activate(self):
        if self.database_garage_item == None: return False
        if self.database_garage_item.count <= 0: return False
        if not self.supplie_timer.is_time_passed(): return False

        self.supplie_timer.start()
        self.subtract_supplie_from_user()
        return True

    def activate_effect(self):
        return
