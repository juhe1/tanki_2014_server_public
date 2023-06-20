from client.layouts.garage.models.upgrade_garage_item_model import upgrade_garage_item_model_command_handler
from client.layouts.garage.models.upgrade_garage_item_model import upgrade_garage_item_model_commands
from client.layouts.garage.models.upgrade_garage_item_model import upgrade_garage_item_model_data
from client.space.model import Model

import threading

class UpgradeGarageItemModel(Model):
    model_id = 300040024

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.model_data = upgrade_garage_item_model_data.UpgradeGarageItemModelData(game_object, client_object)
        self.commands = upgrade_garage_item_model_commands.UpgradeGarageItemModelCommands(client_space, game_object)
        self.command_handler = upgrade_garage_item_model_command_handler.UpgradeGarageItemModelCommandHandler(client_object)
