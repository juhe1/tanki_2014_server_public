from client.dispatcher.codecs import dispatcher_codecs

SWF_LIBRARY = 1

A3D = 2

MOVIE_CLIP = 3

SOUND = 4

MAP = 7

PROP_LIB = 8

MODEL_3DS = 9

IMAGE = 10

MULTIFRAME_IMAGE = 11

LOCALIZED_IMAGE = 13

TANKS_3DS_RESOURCE = 17

LOCALIZATION = 23

def string_to_resource_type(string):
    if string == "swf_library":
        return self.SWF_LIBRARY
    if string == "a3d":
        return self.A3D
    if string == "movie_clip":
        return self.MOVIE_CLIP
    if string == "sound":
        return self.SOUND
    if string == "model_3ds":
        return self.MODEL_3DS
    if string == "image":
        return self.IMAGE
    if string == "multiframe_image":
        return self.MULTIFRAME_IMAGE
    if string == "localized_image":
        return self.LOCALIZED_IMAGE
    if string == "tanks_3ds_resource":
        return self.TANKS_3DS_RESOURCE
    if string == "localization":
        return self.LOCALIZATION
    if string == "map":
        return self.MAP
    if string == "prop_lib":
        return self.PROP_LIB

def get_codec(_type):
    if _type == SWF_LIBRARY:
        return dispatcher_codecs.SwfParamsCodec

    if _type == IMAGE:
        return dispatcher_codecs.ImageParamsCodec

    if _type == LOCALIZATION:
        return dispatcher_codecs.Empty

    if _type == TANKS_3DS_RESOURCE:
        return dispatcher_codecs.Tanks3DSResource

    if _type == LOCALIZED_IMAGE:
        return dispatcher_codecs.Empty

    if _type == MULTIFRAME_IMAGE:
        return dispatcher_codecs.ImageFrameParams

    if _type == MAP:
        return dispatcher_codecs.Empty

    if _type == SOUND:
        return dispatcher_codecs.Empty

    if _type == PROP_LIB:
        return dispatcher_codecs.Empty
