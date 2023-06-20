from client.layouts.battle.models.coloring_model import coloring_model
from space.global_model import GlobalModel

class ColoringGlobalModel(GlobalModel):

    CLIENT_MODEL = coloring_model.ColoringModel

    def __init__(self, global_game_object, global_space, color_resource_name, owner_id=None):
        super().__init__(global_game_object, global_space, owner_id)

        self.color_resource_name = color_resource_name
