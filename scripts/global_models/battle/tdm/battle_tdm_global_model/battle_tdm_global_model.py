from client.layouts.battle.models.battle_tdm_model import battle_tdm_model
from space.global_model import GlobalModel

class BattleTdmGlobalModel(GlobalModel):

    CLIENT_MODEL = battle_tdm_model.BattleTdmModel

    def __init__(self, global_game_object, global_space, owner_id=None):
        super().__init__(global_game_object, global_space, owner_id)
