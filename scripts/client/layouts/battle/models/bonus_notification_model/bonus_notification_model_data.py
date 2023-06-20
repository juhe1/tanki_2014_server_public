from client.dispatcher.dispatcher_model import model_data
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer
from . import bonus_notification_model

class BonusNotificationModelData:
    def __init__(self, bonus_notification_cc):
        self.bonus_notification_cc = bonus_notification_cc

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.OptionalCodec.encode((self.bonus_notification_cc.notification_message, buffer), buffer, basic_codecs.StringCodec)
        basic_codecs.OptionalCodec.encode((self.bonus_notification_cc.sound_notification, buffer), buffer, basic_codecs.LongCodec)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = bonus_notification_model.BonusNotificationModel.model_id
        return _model_data
