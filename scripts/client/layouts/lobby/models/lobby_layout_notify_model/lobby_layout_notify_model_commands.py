from client.layouts.lobby.lobby_enums import Layout
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer
from utils.log import console_out

class LobbyLayoutNotifyModelCommands:
    def __init__(self, space, game_object):
        self.space = space
        self.game_object = game_object

        self.BEGIN_LAYOUT_SWITCH_COMMAND_ID = 300070011
        self.END_LAYOUT_SWITCH_COMMAND_ID = 300070013

    def enum_to_layout_id(self, layout_enum):
        if layout_enum == Layout.BATTLE_SELECT:
            return 0
        elif layout_enum == Layout.GARAGE:
            return 1
        if layout_enum == Layout.PAYMENT:
            return 2
        if layout_enum == Layout.BATTLE:
            return 3
        if layout_enum == Layout.RELOAD_SPACE:
            return 4
        else:
            console_out.color_print('[BEGIN_LAYOUT_SWITCH] layout_enum: "' + str(layout_enum) + '" doesnt exist', "red")

    def begin_layout_switch(self, layout_enum):
        layout_id = self.enum_to_layout_id(layout_enum)

        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.BEGIN_LAYOUT_SWITCH_COMMAND_ID, buffer)
        basic_codecs.IntCodec.encode(layout_id, buffer)
        self.space.send_command(self.game_object.id, buffer, "BEGIN_LAYOUT_SWITCH")

    def end_layout_switch(self, layout_enum):
        layout_id = self.enum_to_layout_id(layout_enum)

        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.END_LAYOUT_SWITCH_COMMAND_ID, buffer)
        basic_codecs.IntCodec.encode(layout_id, buffer)
        self.space.send_command(self.game_object.id, buffer, "END_LAYOUT_SWITCH")
