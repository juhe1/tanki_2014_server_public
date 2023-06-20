from . import bonus_common_model_data
from client.space.model import Model

class BonusCommonModel(Model):
    model_id = 300100015

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.model_data = bonus_common_model_data.BonusCommonModelData(global_model.get_model_data())
