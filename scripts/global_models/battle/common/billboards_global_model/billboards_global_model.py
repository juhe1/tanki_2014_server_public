from client.layouts.battle.models.billboards_model import billboards_model
from loaders.client_resource_loader import client_resource_loader
from space.global_model import GlobalModel
from . import billboards_model_cc
from loaders.server_properties_loader import server_properties_loader

class BillboardsGlobalModel(GlobalModel):

    CLIENT_MODEL = billboards_model.BillboardsModel

    def __init__(self, global_game_object, global_space, owner_id=None):
        super().__init__(global_game_object, global_space, owner_id)

        self.billboards_model_cc = billboards_model_cc.BillboardsModelCC()
        self.billboards_model_cc.bill_image = client_resource_loader.get_resource_id(server_properties_loader.properties.billboard_image_resource)

    def get_model_data(self):
        return self.billboards_model_cc
