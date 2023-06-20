from . import bonus_notification_model_data
from client.space.model import Model

class BonusNotificationModel(Model):
    model_id = 300100016

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.model_data = bonus_notification_model_data.BonusNotificationModelData(global_model.get_model_data())
