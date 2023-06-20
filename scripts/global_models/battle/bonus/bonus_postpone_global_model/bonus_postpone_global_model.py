from client.layouts.battle.models.bonus_postpone_model import bonus_postpone_model
from space.global_model import GlobalModel

class BonusPostponeGlobalModel(GlobalModel):

    CLIENT_MODEL = bonus_postpone_model.BonusPostponeModel

    def __init__(self, global_game_object, global_space, owner_id=None):
        super().__init__(global_game_object, global_space, owner_id)
