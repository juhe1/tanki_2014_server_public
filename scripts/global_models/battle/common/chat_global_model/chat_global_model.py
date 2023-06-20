from client.layouts.battle.models.chat_model import chat_model
from space.global_model import GlobalModel

class ChatGlobalModel(GlobalModel):

    CLIENT_MODEL = chat_model.ChatModel

    def __init__(self, global_game_object, global_space, owner_id=None):
        super().__init__(global_game_object, global_space, owner_id)
