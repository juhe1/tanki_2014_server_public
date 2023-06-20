from global_models.battle.common.battle_field_global_model import battle_field_global_model
from client.layouts.garage.database import database_garage_item_loader
from client.basic_commands import handle_basic_command
from client.basic_commands import basic_commands
from client.space import client_space_registry
from client.dispatcher import resource_loader
from utils.binary.codecs import basic_codecs
from client.space import game_class_registry
from database import user_propertyes_table
from space import global_space_registry
from utils.binary import binary_stream
from database import garage_tables
from utils.log import console_out
import connection_handler
import server_properties

import threading
import weakref
import socket
import time

class Client:
    def __init__(self, client_hash):
        self.main_socket = None

        # create weak object of the real client object, because we want to avoid circle references. with avoiding circle references we avoid memory leaks
        weak_client_object = weakref.ref(self)
        self.weak_client_object = weak_client_object()

        self.client_space_registry = client_space_registry.ClientSpaceRegistry(self.weak_client_object)
        self.basic_commands = basic_commands.BasicCommands(self.weak_client_object)
        self.game_class_registry = game_class_registry.GameClassRegistry(self.weak_client_object)
        self.resource_loader = resource_loader.ResourceLoader(self.weak_client_object)
        self.handle_basic_command = handle_basic_command.HandleBasicCommand(self.weak_client_object)
        self.database_garage_item_loader = database_garage_item_loader.DatabaseGarageItemLoader()

        self.language = ""
        self.locale = ""
        self.client_hash = client_hash
        self.user_id = 0
        self.username = ""
        self.current_battle_global_space = None
        self.user_property_model = None

    def remove_user_from_battle(self):
        if self.current_battle_global_space == None: return
        _battle_field_global_model = self.current_battle_global_space.get_global_model(battle_field_global_model.BattleFieldGlobalModel, global_game_object_name="default_game_object")
        _battle_field_global_model.exit_battle(self.user_id)

    def disconnect(self):
        self.main_socket.shutdown(socket.SHUT_RDWR)

    def remove_client(self):
        self.remove_user_from_battle()
        connection_handler.remove_client(self.client_hash)
        self.client_space_registry.remove_all_spaces() # this is called, because we want to disconnect all spaces

        console_out.color_print("[INFO] removed client", "blue")

    def try_sendall(self, command):
        try:
            self.main_socket.sendall(command)
        except socket.error:
            self.remove_client()
            return False
        return True

    def recive_data(self, channel_id="CLIENT"):
        # recive data from client
        try:
            data = self.main_socket.recv(server_properties.RECEIVE_BUFFER_SIZE)
        except:
            return

        if data == b"":
            return

        # if client recuests policy file then give it
        if data.decode("utf-8", errors="ignore") == "<policy-file-request/>\0":
            # send cross domain
            xml = '<?xml version=\"1.0\"?><cross-domain-policy><allow-access-from domain=\"*\" to-ports=\"*\"/></cross-domain-policy>\0';
            self.try_sendall(bytes(xml, "utf-8"))

        console_out.print_package(data)

        return binary_stream.BinaryStream(data)

    def handle_main_packages(self, socket, address):
        self.main_socket = socket
        self.main_address = address

        while True:
            binary_data = self.recive_data("MAIN CHANNEL")

            if binary_data == None: # delete client object, if we dont recive anything
                self.remove_client()
                return

            binary_datas = basic_codecs.PackageCodec.decode(binary_data)

            for binary_data in binary_datas:
                # parse comman type from package
                command_type = basic_codecs.ByteCodec.decode(binary_data)
                console_out.safe_print("[MAIN] command_type: " + str(command_type))

                thread = threading.Thread(target=self.handle_basic_command.handle_command, args=(command_type, binary_data))
                thread.start() # TODO: make better code that doesnt need thread
