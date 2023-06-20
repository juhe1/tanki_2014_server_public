from client.layouts.battle.models.tank_rank_up_effect_model import tank_rank_up_effect_model
from loaders.client_resource_loader import client_resource_loader
from space.global_model import GlobalModel
from . import tank_rank_up_effect_model_cc

class TankRankUpEffectGlobalModel(GlobalModel):

    CLIENT_MODEL = tank_rank_up_effect_model.TankRankUpEffectModel

    def __init__(self, global_game_object, global_space, owner_id=None):
        super().__init__(global_game_object, global_space, owner_id)

        self.tank_rank_up_effect_model_cc = self.create_cc()

    def create_cc(self):
        _tank_rank_up_effect_model_cc = tank_rank_up_effect_model_cc.TankRankUpEffectModelCC()
        _tank_rank_up_effect_model_cc.rank_up_sound = client_resource_loader.get_resource_id("/battle/sounds/tank/rank_up_sound")
        return _tank_rank_up_effect_model_cc

    def get_model_data(self):
        return self.tank_rank_up_effect_model_cc
