from client.dispatcher import class_dispatcher_item
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class GameClassRegistry:
    def __init__(self, client_object):
        self.client_object = client_object
        self.game_classes = {}

    # get game_class key with game_calss id
    def get_game_class_key_by_id(self, id):
        for key, game_class in self.game_classes.items():
            if game_class.class_id == id: return key

    def update_class(self, game_models, class_id):
        model_ids = [game_model.model_id for game_model in game_models] # get model ids from models and put them into list
        model_ids.sort() # sort the list, because we dont want that the item order affects our if statement bellow
        model_ids = tuple(model_ids) # lists cant bee usen as keys so we need to convert it

        model_datas = binary_buffer.BinaryBuffer()
        basic_codecs.IntCodec.encode(0, model_datas) # model_data count

        # make new game_class
        new_class_dispatcher_item = class_dispatcher_item.ClassDispatcherItem()
        new_class_dispatcher_item.class_id = class_id
        new_class_dispatcher_item.parrent_id = None
        new_class_dispatcher_item.game_model_ids = list(model_ids)
        new_class_dispatcher_item.model_datas = model_datas

        # update game class key and class
        game_calss_key = self.get_game_class_key_by_id(class_id)
        self.game_classes.pop(game_calss_key)
        self.game_classes[model_ids] = new_class_dispatcher_item

        self.client_object.basic_commands.load_dependencies([new_class_dispatcher_item])
        self.client_object.handle_basic_command.recive_dependencies_loaded_command()

        return class_id

    # TODO: remove "_and_chost_model" from the name
    def create_class_from_models_and_chost_model(self, game_models):
        model_ids = [game_model.model_id for game_model in game_models] # get model ids from models and put them into list
        model_ids.sort() # sort the list, because we dont want that the item order affects our if statement bellow
        model_ids = tuple(model_ids) # lists cant bee usen as keys so we need to convert it

        # if already have game_class that has same models then return it
        if model_ids in self.game_classes:
            return self.game_classes[model_ids].class_id

        last_class_id = -1
        if not self.game_classes == {}:
            game_class_ids = list(self.game_classes.values())
            last_class_id = game_class_ids[-1].class_id

        model_datas = binary_buffer.BinaryBuffer()
        basic_codecs.IntCodec.encode(0, model_datas) # model_data count

        # make new game_class
        new_class_dispatcher_item = class_dispatcher_item.ClassDispatcherItem()
        new_class_dispatcher_item.class_id = last_class_id + 1
        new_class_dispatcher_item.parrent_id = None
        new_class_dispatcher_item.game_model_ids = list(model_ids)
        new_class_dispatcher_item.model_datas = model_datas

        self.game_classes[model_ids] = new_class_dispatcher_item # we use game model ids as key
        self.client_object.basic_commands.load_dependencies([new_class_dispatcher_item])
        self.client_object.handle_basic_command.recive_dependencies_loaded_command()

        return last_class_id + 1
