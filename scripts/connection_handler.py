from utils.binary.codecs import basic_codecs
from space import global_space_registry
from utils.binary import binary_stream
from utils.log import console_out
from client import client
import server_properties

import threading
import secrets
import hexdump
import socket

clients_by_hash = {}
connection_id = 0

def init():
    create_main_connection_handlers()
    create_space_connection_handlers()

def create_main_connection_handlers():
    for port in server_properties.PORTS:
        # create main socket
        main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        main_socket.settimeout(None)
        main_socket.bind((server_properties.IP, port))
        main_socket.listen(server_properties.MAX_PLAYER_COUNT)

        # create thread for handle_main_connections
        thread = threading.Thread(target=handle_main_connections, args=(main_socket,))
        thread.start()

def create_space_connection_handlers():
    for port in server_properties.SPACE_PORTS:
        # create space socket
        space_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        space_socket.bind((server_properties.IP, port))
        space_socket.listen(server_properties.MAX_PLAYER_COUNT * 4)

        # create thread for handle_space_connections
        thread = threading.Thread(target=handle_space_connections, args=(space_socket,))
        thread.start()

def remove_client(client_hash):
    global clients_by_hash

    if not client_hash in clients_by_hash: return
    clients_by_hash.pop(client_hash, None)

def recive_hash(socket):
    while True:

        try:
            package = socket.recv(server_properties.RECEIVE_BUFFER_SIZE) # recive data from client
        except:
            return

        if package == b"": return

        # if client recuests policy file then give it
        if package.decode("utf-8", errors="ignore") == "<policy-file-request/>\0":
            # send cross domain policy file
            xml = '<?xml version="1.0"?><cross-domain-policy><allow-access-from domain="*" to-ports="*"/></cross-domain-policy>\0'

            socket.sendall(bytes(xml, "utf-8"))
            continue

        binary_data = binary_stream.BinaryStream(package)
        binary_datas = basic_codecs.PackageCodec.decode(binary_data)

        for binary_data in binary_datas:
            command_type = basic_codecs.ByteCodec.decode(binary_data) # parse command type from package
            if command_type == 3:
                return binary_data.read_bytes(32)
            else:
                return

def handle_space_connection(socket, address):
    hash = recive_hash(socket)
    if hash not in clients_by_hash: return

    client_object = clients_by_hash[hash]

    for global_space in global_space_registry.get_all_spaces():
        succeed = global_space.try_connecting_new_client(client_object, socket, address)
        if succeed: return

    # disconnect client, if we didnt succeed on connecting the user to space
    client_object.disconnect()

def handle_space_connections(space_socket):
    while True:
        socket, address = space_socket.accept()

        # tis need to be done in another thread, because reciving the hash will take some time
        thread = threading.Thread(target=handle_space_connection, args=(socket, address))
        thread.start()

def handle_main_connections(main_socket):
    global clients_by_hash, connection_id

    while True:
        socket, address = main_socket.accept()
        console_out.log_print(f"client connected to main from {address}")
        connection_id += 1

        # set connection_id back to 0 if it is int max number
        if connection_id == 0xffff:
            connection_id = 0

        # we add the connection_id, because we dont want accidentally create hash that some one else has
        client_hash = secrets.token_bytes(28) + connection_id.to_bytes(4, 'big', signed=True)

        # create clinet object
        clien_object = client.Client(client_hash)

        # start handle_main_packages thread from client
        handle_client_thread = threading.Thread(target=clien_object.handle_main_packages, args=(socket, address))
        handle_client_thread.start()

        # add user into clients_by_hash dictionary, because we want later know who is connecting to space
        clients_by_hash[client_hash] = clien_object
