from client.layouts.battle.models.discrete_shot_model import discrete_shot_model
from space.global_model import GlobalModel
from . import discrete_shot_model_cc

class DiscreteShotGlobalModel(GlobalModel):

    CLIENT_MODEL = discrete_shot_model.DiscreteShotModel

    def __init__(self, global_game_object, global_space, turret_database_item, owner_id=None):
        super().__init__(global_game_object, global_space, owner_id)
        self.turret_database_item = turret_database_item
        self.turret_garage_item = turret_database_item.garage_item

        self.discrete_shot_model_cc = self.create_discrete_shot_model_cc()

    def create_discrete_shot_model_cc(self):
        _discrete_shot_model_cc = discrete_shot_model_cc.DiscreteShotModelCC()
        _discrete_shot_model_cc.auto_aiming_angle_down = self.turret_garage_item.discrete_shot_data.auto_aiming_angle_down
        _discrete_shot_model_cc.auto_aiming_angle_up = self.turret_garage_item.discrete_shot_data.auto_aiming_angle_up
        _discrete_shot_model_cc.reload_msec = self.turret_database_item.get_property_value("weapon_reload_time")
        return _discrete_shot_model_cc

    def get_model_data(self):
        return self.discrete_shot_model_cc
