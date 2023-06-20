from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class SmokyModelCommands:
    def __init__(self, space, game_object):
        self.space = space
        self.game_object = game_object
        self.SHOOT_COMMAND_ID = 300100078
        self.SHOOT_STATIC_COMMAND_ID = 300100079
        self.SHOOT_TARGET_COMMAND_ID = 300100080
        self.LOCAL_CRITICAL_HIT_COMMAND_ID = 300100077

    def shoot(self, shooter_id):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.SHOOT_COMMAND_ID, buffer)
        basic_codecs.LongCodec.encode(shooter_id, buffer)
        self.space.send_command(self.game_object.id, buffer, "SHOOT")

    def shoot_static(self, shooter_id, hit_point):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.SHOOT_STATIC_COMMAND_ID, buffer)
        basic_codecs.LongCodec.encode(shooter_id, buffer)
        basic_codecs.Vector3DCodec.encode(hit_point, buffer)
        self.space.send_command(self.game_object.id, buffer, "SHOOT_STATIC")

    def shoot_target(self, shooter_id, target_id, hit_point, weakening_coff, is_critical_hit):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.SHOOT_TARGET_COMMAND_ID, buffer)
        basic_codecs.LongCodec.encode(shooter_id, buffer)
        basic_codecs.LongCodec.encode(target_id, buffer)
        basic_codecs.Vector3DCodec.encode(hit_point, buffer)
        basic_codecs.FloatCodec.encode(weakening_coff, buffer)
        basic_codecs.BooleanCodec.encode(is_critical_hit, buffer)
        self.space.send_command(self.game_object.id, buffer, "SHOOT_TARGET")

    def local_critical_hit(self, target_id):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.LOCAL_CRITICAL_HIT_COMMAND_ID, buffer)
        basic_codecs.LongCodec.encode(target_id, buffer)
        self.space.send_command(self.game_object.id, buffer, "LOCAL_CRITICAL_HIT")
