from loaders.client_resource_loader import client_resource_loader
import server_properties

class BonusCommonModelCC:
    def __init__(self):
        self.box_resource = 0
        self.cord_resource = client_resource_loader.get_resource_id("/battle/images/cord")
        self.life_time = 0
        self.parachute_inner_resource = client_resource_loader.get_resource_id("/battle/3ds/bonuses/parachute_inner")
        self.parachute_resource = client_resource_loader.get_resource_id("/battle/3ds/bonuses/parachute")
        self.pickup_sound_resource = client_resource_loader.get_resource_id("/battle/sounds/bonus_take")
