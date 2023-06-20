from utils.binary.codecs import basic_codecs

class UidNotifierDataCodec:
    def encode(user_info, buffer):
        basic_codecs.StringCodec.encode(user_info.uid, buffer)
        basic_codecs.LongCodec.encode(user_info.user_id, buffer)


class RankNotifierDataCodec:
    def encode(user_info, buffer):
        basic_codecs.IntCodec.encode(user_info.rank, buffer)
        basic_codecs.LongCodec.encode(user_info.user_id, buffer)

