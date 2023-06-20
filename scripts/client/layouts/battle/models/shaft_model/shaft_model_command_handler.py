from utils.binary.codecs import basic_codecs

class ShaftModelCommandHandler:
    def __init__(self, shaft_global_model):
        self.shaft_global_model = shaft_global_model

        self.ACTIVATE_MANUAL_TARGETING_COMMAND_ID = 300100065
        self.AIMED_SHOT_COMMAND_ID = 300100066
        self.BEGIN_ENERGY_DRAIN_COMMAND_ID = 300100067
        self.QUICK_SHOT_COMMAND_ID = 300100068
        self.STOP_MANUAL_TARGETING_COMMAND_ID = 300100069

    def handle_command(self, binary_data, command_id):
        if command_id == self.ACTIVATE_MANUAL_TARGETING_COMMAND_ID:
            self.activate_manual_targeting()
            return True

        if command_id == self.AIMED_SHOT_COMMAND_ID:
            self.aimed_shot(binary_data)
            return True

        if command_id == self.BEGIN_ENERGY_DRAIN_COMMAND_ID:
            self.begin_energy_drain()
            return True

        if command_id == self.QUICK_SHOT_COMMAND_ID:
            self.quick_shot(binary_data)
            return True

        if command_id == self.STOP_MANUAL_TARGETING_COMMAND_ID:
            self.stop_manual_targeting()
            return True

    def activate_manual_targeting(self):
        self.shaft_global_model.activate_manual_targeting()

    def aimed_shot(self, binary_data):
        time = basic_codecs.IntCodec.decode(binary_data)
        static_hit_point = basic_codecs.OptionalCodec.decode((binary_data,), binary_data, basic_codecs.Vector3DCodec)
        target_ids = basic_codecs.OptionalCodec.decode((binary_data, basic_codecs.LongCodec), binary_data, basic_codecs.VectorLevel1Codec)
        target_hit_points = basic_codecs.OptionalCodec.decode((binary_data, basic_codecs.Vector3DCodec), binary_data, basic_codecs.VectorLevel1Codec)
        target_incarnations = basic_codecs.OptionalCodec.decode((binary_data, basic_codecs.ShortCodec), binary_data, basic_codecs.VectorLevel1Codec)
        target_positions = basic_codecs.OptionalCodec.decode((binary_data, basic_codecs.Vector3DCodec), binary_data, basic_codecs.VectorLevel1Codec)
        hit_points = basic_codecs.OptionalCodec.decode((binary_data, basic_codecs.Vector3DCodec), binary_data, basic_codecs.VectorLevel1Codec)
        self.shaft_global_model.aimed_shot(time, static_hit_point, target_ids, target_hit_points, target_incarnations, target_positions, hit_points)

    def begin_energy_drain(self):
        self.shaft_global_model.begin_energy_drain()

    def quick_shot(self, binary_data):
        time = basic_codecs.IntCodec.decode(binary_data)
        static_hit_point = basic_codecs.OptionalCodec.decode((binary_data,), binary_data, basic_codecs.Vector3DCodec)
        target_ids = basic_codecs.OptionalCodec.decode((binary_data, basic_codecs.LongCodec), binary_data, basic_codecs.VectorLevel1Codec)
        target_hit_points = basic_codecs.OptionalCodec.decode((binary_data, basic_codecs.Vector3DCodec), binary_data, basic_codecs.VectorLevel1Codec)
        target_incarnations = basic_codecs.OptionalCodec.decode((binary_data, basic_codecs.ShortCodec), binary_data, basic_codecs.VectorLevel1Codec)
        target_positions = basic_codecs.OptionalCodec.decode((binary_data, basic_codecs.Vector3DCodec), binary_data, basic_codecs.VectorLevel1Codec)
        hit_points = basic_codecs.OptionalCodec.decode((binary_data, basic_codecs.Vector3DCodec), binary_data, basic_codecs.VectorLevel1Codec)
        self.shaft_global_model.quick_shot(time, static_hit_point, target_ids, target_hit_points, target_incarnations, target_positions, hit_points)

    def stop_manual_targeting(self):
        self.shaft_global_model.stop_manual_targeting()
