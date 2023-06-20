from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class BattleMinesModelCommands:
    def __init__(self, space, game_object):
        self.space = space
        self.game_object = game_object
        self.ACTIVATE_MINE_COMMAND_ID = 300100001
        self.EXPLODE_MINE_COMMAND_ID = 300100002
        self.PUT_MINE_COMMAND_ID = 300100003
        self.REMOVE_MINES_COMMAND_ID = 300100004

    def activate_mine(self, mine_id):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.ACTIVATE_MINE_COMMAND_ID, buffer)
        basic_codecs.LongCodec.encode(mine_id, buffer)
        self.space.send_command(self.game_object.id, buffer, "ACTIVATE_MINE")

    def explode_mine(self, mine_id, target_id):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.EXPLODE_MINE_COMMAND_ID, buffer)
        basic_codecs.LongCodec.encode(mine_id, buffer)
        basic_codecs.LongCodec.encode(target_id, buffer)
        self.space.send_command(self.game_object.id, buffer, "EXPLODE_MINE")

    def put_mine(self, mine_id, mine_pos, user_id):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.PUT_MINE_COMMAND_ID, buffer)
        basic_codecs.LongCodec.encode(mine_id, buffer)
        basic_codecs.Vector3DCodec.encode(mine_pos, buffer)
        basic_codecs.LongCodec.encode(user_id, buffer)
        self.space.send_command(self.game_object.id, buffer, "PUT_MINE")

    def remove_mines(self, owner_id):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.REMOVE_MINES_COMMAND_ID, buffer)
        basic_codecs.LongCodec.encode(owner_id, buffer)
        self.space.send_command(self.game_object.id, buffer, "REMOVE_MINES")
