from loaders.client_resource_loader import client_resource_loader

class BattleMinesModelCC:
    def __init__(self):
        self.activate_sound = client_resource_loader.get_resource_id("/battle/sounds/mine/activate")
        self.battle_mines = None
        self.blue_mine_texture = client_resource_loader.get_resource_id("/battle/images/mine/blue_mine")
        self.deactivate_sound = client_resource_loader.get_resource_id("/battle/sounds/mine/deactivate")
        self.empty_mine_texture = client_resource_loader.get_resource_id("/battle/images/mine/empty_mine")
        self.explosion_mark_texture = client_resource_loader.get_resource_id("/battle/images/mine/explosion_mark")
        self.explosion_sound = client_resource_loader.get_resource_id("/battle/sounds/mine/explosion")
        self.friendly_mine_texture = client_resource_loader.get_resource_id("/battle/images/mine/friendly_mine")
        self.idle_explosion_texture = client_resource_loader.get_resource_id("/battle/multiframe_image/mine/idle_explosion")
        self.main_explosion_texture = client_resource_loader.get_resource_id("/battle/multiframe_image/mine/main_explosion")
        self.model3ds = client_resource_loader.get_resource_id("/battle/3ds/mine_model")
        self.red_mine_texture = client_resource_loader.get_resource_id("/battle/images/mine/red_mine")
