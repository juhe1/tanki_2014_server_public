from client.layouts.battle.models.isis_model import isis_model
from space.global_model import GlobalModel
from . import isis_model_cc

class IsisGlobalModel(GlobalModel):

    CLIENT_MODEL = isis_model.IsisModel

    def __init__(self, global_game_object, global_space, turret_database_item, owner_id=None):
        super().__init__(global_game_object, global_space, owner_id)

        self.turret_database_item = turret_database_item
        self.isis_data = turret_database_item.garage_item.isis_data
        self.isis_model_cc = self.create_cc()

    def create_cc(self):
        cc = isis_model_cc.IsisModelCC()
        cc.angle = self.isis_data.healing_angle
        cc.capacity = self.isis_data.capacity
        cc.charge_rate = cc.capacity / self.turret_database_item.get_property_value("weapon_reload_time")
        cc.check_period_msec = self.isis_data.weapon_tick_interval_msec
        cc.cone_angle = self.isis_data.cone_angle
        cc.discharge_rate = self.isis_data.discharge_rate
        cc.radius = self.isis_data.radius
        return cc

    def get_model_data(self):
        return self.isis_model_cc
