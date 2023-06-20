from client.layouts.battle.models.bcsh_model import bcsh_model
from space.global_model import GlobalModel
from . import bcsh_model_cc

class BcshGlobalModel(GlobalModel):

    CLIENT_MODEL = bcsh_model.BcshModel

    def __init__(self, global_game_object, global_space, bcsh_data, owner_id=None):
        super().__init__(global_game_object, global_space, owner_id)

        self.bcsh_model_cc = bcsh_model_cc.BcshModelCC()
        self.bcsh_model_cc.bcsh_data = bcsh_data

    def get_model_data(self):
        return self.bcsh_model_cc
