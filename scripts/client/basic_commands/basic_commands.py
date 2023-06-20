from loaders.client_resource_loader import resource_types
from client.dispatcher.codecs import dispatcher_codecs
from utils.binary.codecs import basic_codecs
from space import global_space_registry
from utils.binary import binary_buffer
from utils.log import console_out
from . import basic_command_types
import server_properties

# basic commands are commands that will be send with main socket(the socket that client will first connect)

class BasicCommands:
    def __init__(self, client_object):
        self.client_object = client_object

    def send_hash_response(self, use_xor_protection, _hash):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.ByteCodec.encode(basic_command_types.SV_HASH_RESPONSE, buffer)

        buffer.write_bytes(_hash)
        buffer.add_type([console_out.BACKGROUND_COLORS["black"], 32])
        basic_codecs.BooleanCodec.encode(use_xor_protection, buffer)

        basic_codecs.PackageCodec.encode(buffer)
        console_out.print_server_package(buffer, "HASH RESPONSE PACKAGE")
        self.client_object.try_sendall(buffer.get_binary_data())

    def load_dependencies(self, dispatcher_items):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.ByteCodec.encode(basic_command_types.SV_LOAD_DEPENDENCIES, buffer)
        basic_codecs.IntCodec.encode(len(dispatcher_items), buffer)
        for dispatcher_item in dispatcher_items:
            dispatcher_codecs.DispatcherItemCodec.encode(dispatcher_item, buffer)

        basic_codecs.PackageCodec.encode(buffer)
        console_out.print_server_package(buffer, "LOAD DEPENCIES COMMAND")
        self.client_object.try_sendall(buffer.get_binary_data())

    def open_space(self, space_name):
        global_space = global_space_registry.get_space_by_name(space_name)
        global_space.add_connecting_client(self.client_object)

        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.ByteCodec.encode(basic_command_types.SV_OPEN_SPACE, buffer)
        basic_codecs.LongCodec.encode(global_space.id, buffer)
        basic_codecs.StringCodec.encode(server_properties.SPACE_IP, buffer)
        basic_codecs.ByteCodec.encode(len([server_properties.NGROK_SPACE_PORTS]), buffer)

        for port in server_properties.NGROK_SPACE_PORTS:
            basic_codecs.IntCodec.encode(port, buffer)

        basic_codecs.PackageCodec.encode(buffer)
        console_out.print_server_package(buffer, "OPEN SPACE COMMAND")
        self.client_object.try_sendall(buffer.get_binary_data())
        return self.client_object.client_space_registry.wait_for_space(space_name)
