from client.dispatcher.codecs import dispatcher_codecs
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer
from utils.log import console_out

class DispatcherModelCommands:
    def __init__(self, space, game_object):
        self.space = space
        self.game_object = game_object
        self.load_objects_command_id = 100000
        self.unload_objects_command_id = 100001

    def load_objects(self, object_structs):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.load_objects_command_id, buffer)
        basic_codecs.VectorLevel1Codec.encode(object_structs, dispatcher_codecs.LoadObjectStructCodec, buffer)
        self.space.send_command(self.game_object.id, buffer, "LOAD OBJECT COMMAND")


    def unload_objects(self, object_ids):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.unload_objects_command_id, buffer)
        basic_codecs.VectorLevel1Codec.encode(object_ids, basic_codecs.LongCodec, buffer)
        self.space.send_command(self.game_object.id, buffer, "UNLOAD OBJECT COMMAND")
