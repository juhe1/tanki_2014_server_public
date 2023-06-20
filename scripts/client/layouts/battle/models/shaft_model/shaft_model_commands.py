from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class ShaftModelCommands:
    def __init__(self, space, game_object):
        self.space = space
        self.game_object = game_object
        self.FIRE_COMMAND_ID = 300100071
        self.ACTIVATE_MANUAL_TARGETING_COMMAND_ID = 300100070
        self.STOP_MANUAL_TARGETING_COMMAND_ID = 300100072

    def fire(self, shooter_id, hit_point, target_ids, target_hitpoints, impact_force):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.FIRE_COMMAND_ID, buffer)
        basic_codecs.LongCodec.encode(shooter_id, buffer)
        basic_codecs.OptionalCodec.encode((hit_point, buffer), buffer, basic_codecs.Vector3DCodec)
        basic_codecs.OptionalCodec.encode((target_ids, basic_codecs.LongCodec, buffer), buffer, basic_codecs.VectorLevel1Codec)
        basic_codecs.OptionalCodec.encode((target_hitpoints, basic_codecs.Vector3DCodec, buffer), buffer, basic_codecs.VectorLevel1Codec)
        basic_codecs.FloatCodec.encode(impact_force, buffer)
        self.space.send_command(self.game_object.id, buffer, "FIRE")

    def activate_manual_targeting(self, shooter_id):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.ACTIVATE_MANUAL_TARGETING_COMMAND_ID, buffer)
        basic_codecs.LongCodec.encode(shooter_id, buffer)
        self.space.send_command(self.game_object.id, buffer, "ACTIVATE_MANUAL_TARGETING")

    def stop_manual_targeting(self, shooter_id):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.STOP_MANUAL_TARGETING_COMMAND_ID, buffer)
        basic_codecs.LongCodec.encode(shooter_id, buffer)
        self.space.send_command(self.game_object.id, buffer, "STOP_MANUAL_TARGETING")
