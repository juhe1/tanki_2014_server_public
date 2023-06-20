from client.space.model import Model
from . import billboards_model_data

class BillboardsModel(Model):
    model_id = 300100011

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.model_data = billboards_model_data.BillboardsModelData(game_object, global_model.get_model_data())
        self.commands = None
        self.command_handler = None
