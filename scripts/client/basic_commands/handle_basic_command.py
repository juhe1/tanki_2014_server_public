from client.layouts.entrance.models.entrance_model import entrance_model
from client.dispatcher.dispatcher_model import dispatcher_model
from utils.binary.codecs import basic_codecs
from . import basic_command_types
from utils.log import console_out

import time

class HandleBasicCommand:
    def __init__(self, client_object):
        self.commands = Commands(client_object)
        self.depencie_loaded = False

    def recive_dependencies_loaded_command(self):
        while self.depencie_loaded == False:
            time.sleep(0.1)
        self.depencie_loaded = False

    def handle_command(self, command_type, binary_data):
        if command_type == basic_command_types.CL_HASH_REQUEST:
            self.commands.handle_hash_recuest(binary_data)

        if command_type == basic_command_types.CL_DEPENDENCIES_LOADED:
            self.depencie_loaded = True


class Commands:
    def __init__(self, client_object):
        self.client_object = client_object

    def handle_hash_recuest(self, binary_data):
        keys = basic_codecs.VectorLevel1Codec.decode(binary_data, basic_codecs.StringCodec)
        values = basic_codecs.VectorLevel1Codec.decode(binary_data, basic_codecs.StringCodec)

        config_url = values[ keys.index("config") ]

        self.client_object.language = values[ keys.index("lang") ]
        self.client_object.locale = values[ keys.index("locale") ]

        self.client_object.basic_commands.send_hash_response(False, self.client_object.client_hash)
        entrance_space = self.client_object.basic_commands.open_space("entrance")

        entrance_object = entrance_space.add_game_object(game_object_name="entrance")
        entrance_object.add_model(entrance_model.EntranceModel)
