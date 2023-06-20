from client.layouts.battle.models.battle_dm_model import battle_dm_model
from space.global_model import GlobalModel

class BattleDmGlobalModel(GlobalModel):

    CLIENT_MODEL = battle_dm_model.BattleDmModel

    def __init__(self, global_game_object, global_space, owner_id=None):
        super().__init__(global_game_object, global_space, owner_id)
