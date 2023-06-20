from utils.binary.codecs import basic_codecs

class BattleFieldBonusModelCommandHandler:
    def __init__(self, global_model, user_id):
        self.global_model = global_model
        self.user_id = user_id

        self.ATTEMPT_TO_TAKE_BONUS_COMMAND_ID = 300100005

    def handle_command(self, binary_data, command_id):
        if command_id == self.ATTEMPT_TO_TAKE_BONUS_COMMAND_ID:
            self.attempt_to_take_bonus(binary_data)
            return True

    def attempt_to_take_bonus(self, binary_buffer):
        bonus_id = basic_codecs.LongCodec.decode(binary_buffer)
        self.global_model.attempt_to_take_bonus(bonus_id, self.user_id)
