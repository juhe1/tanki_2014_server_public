from client.layouts.battle.models.object_3ds_model import object_3ds_model
from space.global_model import GlobalModel

class Object3DSGlobalModel(GlobalModel):

    CLIENT_MODEL = object_3ds_model.Object3DSModel

    def __init__(self, global_game_object, global_space, _3ds_resource_name, owner_id=None):
        super().__init__(global_game_object, global_space, owner_id)

        self._3ds_resource_name = _3ds_resource_name
