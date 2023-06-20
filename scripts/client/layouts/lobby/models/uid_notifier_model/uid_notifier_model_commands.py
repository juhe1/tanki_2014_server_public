from client.layouts.lobby import lobby_codecs
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class UidNotifierModelCommands:
    def __init__(self, space, game_object):
        self.space = space
        self.game_object = game_object

        self.SET_UID_COMMAND_ID = 300150005

    def set_uid(self, user_infos):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.SET_UID_COMMAND_ID, buffer)
        basic_codecs.VectorLevel1Codec.encode(user_infos, lobby_codecs.UidNotifierDataCodec, buffer)
        self.space.send_command(self.game_object.id, buffer, "SET_UID")
