from client.layouts.battle.models.battle_debug_model import battle_debug_model
from space.global_model import GlobalModel

class BattleDebugGlobalModel(GlobalModel):

    CLIENT_MODEL = battle_debug_model.BattleDebugModel

    def __init__(self, global_game_object, global_space, owner_id=None):
        super().__init__(global_game_object, global_space, owner_id)
