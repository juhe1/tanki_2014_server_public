from utils.binary.codecs import basic_codecs

class InventoryItemModelCommandHandler:
    def __init__(self, inventory_item_model):
        self.inventory_item_model = inventory_item_model
        self.ACTIVATE_COMMAND_ID = 300100048

    def handle_command(self, binary_data, command_id):
        if command_id == self.ACTIVATE_COMMAND_ID:
            self.activate()
            return True

    def activate(self):
        succes = self.inventory_item_model.try_activate()
        if succes:
            self.inventory_item_model.activate_effect()
            self.inventory_item_model.commands.activate()
