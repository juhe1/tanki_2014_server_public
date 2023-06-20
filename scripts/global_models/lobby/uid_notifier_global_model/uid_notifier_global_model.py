from client.layouts.lobby.models.uid_notifier_model import uid_notifier_model
from space.global_model import GlobalModel

class UidNotifierGlobalModel(GlobalModel):

    CLIENT_MODEL = uid_notifier_model.UidNotifierModel

    def __init__(self, global_game_object, global_space, owner_id=None):
        super().__init__(global_game_object, global_space, owner_id)
        self.user_infos = []

    def add_uid(self, user_info):
        self.user_infos.append(user_info)
        self.set_uids()

    def set_uids(self):
        self.broadcast_command("set_uid", (self.user_infos,))
