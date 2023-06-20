from global_models.battle.common.color_transform_global_model import color_transform_model_cc
from client.layouts.battle.models.color_transform_model import color_transform_model
from space.global_model import GlobalModel

class ColorTransformGlobalModel(GlobalModel):

    CLIENT_MODEL = color_transform_model.ColorTransformModel

    def __init__(self, global_game_object, global_space, color_transform_structs, owner_id=None):
        super().__init__(global_game_object, global_space, owner_id)

        self.color_transform_model_cc = color_transform_model_cc.ColorTransformModelCC()
        self.color_transform_model_cc.color_transforms = color_transform_structs

    def get_model_data(self):
        return self.color_transform_model_cc
