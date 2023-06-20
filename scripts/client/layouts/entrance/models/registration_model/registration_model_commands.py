from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class RegistrationModelCommands:
    def __init__(self, space, game_object):
        self.space = space
        self.game_object = game_object
        self.ENTERED_UID_IS_INCORRECT_COMMAND_ID = 300020065
        self.ENTERED_UID_IS_FREE_COMMAND_ID = 300020064

    def entered_uid_is_free(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.ENTERED_UID_IS_FREE_COMMAND_ID, buffer)
        self.space.send_command(self.game_object.id, buffer, "ENTERED_UID_IS_FREE")

    def entered_uid_is_incorrect(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.ENTERED_UID_IS_INCORRECT_COMMAND_ID, buffer)
        self.space.send_command(self.game_object.id, buffer, "ENTERED_UID_IS_INCORRECT")
