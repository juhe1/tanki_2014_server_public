from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class BonusPostponeModelCommands:
    def __init__(self, space, game_object):
        self.space = space
        self.game_object = game_object
        self.NOTIFICATION_BONUS_COMMAND_ID = 300100018

    def notification_bonus(self, bonus_notification_model_id):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.NOTIFICATION_BONUS_COMMAND_ID, buffer)
        basic_codecs.LongCodec.encode(bonus_notification_model_id, buffer)
        self.space.send_command(self.game_object.id, buffer, "NOTIFICATION_BONUS")
