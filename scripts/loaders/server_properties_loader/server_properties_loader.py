from loaders.json_loader import cache_json_read
from utils.log import console_out

class ServerPropertiesData:
    def __init__(self, property_data):
        self.__dict__ = property_data

properties = None

def init(path):
    global properties
    property_data = cache_json_read(path)
    properties = ServerPropertiesData(property_data)
    console_out.color_print("[SERVER_PROPERTIES_LOADER] PROPERTIES_LOADED", "yellow")
