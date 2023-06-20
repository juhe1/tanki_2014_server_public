from global_models.battle.bonus.bonus_postpone_global_model import bonus_postpone_global_model
from client.layouts.battle.models.bonus_notification_model import bonus_notification_model
from space.global_model import GlobalModel
from . import bonus_notification_model_cc

class BonusNotificationGlobalModel(GlobalModel):

    CLIENT_MODEL = bonus_notification_model.BonusNotificationModel

    def __init__(self, global_game_object, global_space, model_cc, owner_id=None):
        super().__init__(global_game_object, global_space, owner_id)

        self.model_cc = model_cc
        self.bonus_postpone = self.global_space.get_global_model(bonus_postpone_global_model.BonusPostponeGlobalModel, global_game_object_name="default_game_object")

    def get_model_data(self):
        return self.model_cc

    def send_notification(self):
        self.bonus_postpone.broadcast_command("notification_bonus", (self.global_game_object.id,))
