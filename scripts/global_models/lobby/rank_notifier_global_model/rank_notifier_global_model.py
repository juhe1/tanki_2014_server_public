from client.layouts.lobby.models.rank_notifier_model import rank_notifier_model
from space.global_model import GlobalModel

class RankNotifierGlobalModel(GlobalModel):

    CLIENT_MODEL = rank_notifier_model.RankNotifierModel

    def __init__(self, global_game_object, global_space, owner_id=None):
        super().__init__(global_game_object, global_space, owner_id)
        self.user_infos = []

    def add_rank(self, user_info):
        self.user_infos.append(user_info)
        self.set_ranks()

    def set_ranks(self):
        self.broadcast_command("set_rank", (self.user_infos,))
