from . import resource_dispatcher_item
from . import resource_file_info
from . import resource_types
from loaders import json_loader

import os

RESOURCES_PATH = r"client_resources/"
path_to_id = None

resource_object_by_path_version_and_language = {} # {(path, ver, lang):OBJ}
resource_objects_by_path = {} # {path:[OBJ,OBJ,OBJ...]}

def init():
    global path_to_id
    path_to_id = json_loader.get_json_file_data("path_to_id.json")

def get_resource_id(resource_path):
    return path_to_id[resource_path]

# list all folders that doesn't have folder in it
def list_folderless_folders(dir):
    return [root for root, dirs, files in os.walk(dir) if dirs == []]

# basicly this will do this: ["0_nfsdf", "2_nfsdf", "1_nfsdf"] -> ["0_nfsdf", "1_nfsdf", "2_nfsdf"]
def sort_file_names(file_names):
    pos = -1
    new_list = [""] * len(file_names)

    for file_name in file_names:
        file_name_splitted = file_name.split("_")
        file_index_sring = file_name_splitted[0] # "3_file_name" -> 3

        if file_index_sring.isnumeric() and len(file_name_splitted) > 1:
            new_list[int(file_index_sring)] = file_name
            continue

        new_list[pos] = file_name
        pos -= 1

    return new_list

def is_resource_folder(path):
    # in every resource folder there is empty file named "RESOURCE"
    all_folders_in_path = next(os.walk(path))[1]

    if all_folders_in_path == []:
        return False
        
    return os.path.isfile(path + "/" + all_folders_in_path[0]  + "/resource_info.json")

# we want that these resource_folder_paths are in specific order thats why this function is so complicated
def get_resource_folder_paths_from_path(path):

    if is_resource_folder(path):
        return [path]

    resource_folder_paths = []

    def loop_folders(_path):
        files_and_folders_sorted = sort_file_names( os.listdir(_path) )
        for file in files_and_folders_sorted:
            new_path = os.path.join(_path, file)

            if not is_resource_folder(new_path):
                if os.path.isdir(new_path):
                    # loop path if it is folder and if it is not resource
                    loop_folders(new_path)
            else:
                resource_folder_paths.append(new_path)

    loop_folders(path)
    return resource_folder_paths

def get_resource_objects(resource_path, version=None, language="en"):
    path = os.path.join(RESOURCES_PATH, resource_path)
    global resource_objects_by_path

    if path in resource_objects_by_path:
        return resource_objects_by_path[path]

    resource_folder_paths = get_resource_folder_paths_from_path(path)

    resource_objects = []

    for resource_folder_path in resource_folder_paths:
        resource_objects.append(get_resource_object(resource_folder_path, version, language))

    resource_objects_by_path[path] = resource_objects
    return resource_objects

def create_empty_resource_info(resource_name, file_path):
    file_info = resource_file_info.ResourceFileInfo()
    file_info.file_name = resource_name
    file_info.file_size = os.path.getsize(file_path)
    return file_info

def set_default_params(resource_object, file_name, file_path, file_type):
    file_path = os.path.join(file_path, file_name)
    file_info = create_empty_resource_info(file_name, file_path)

    resource_object.file_infos = [file_info]
    resource_object.type = file_type

def set_params_from_resource_files(resource_folder_path, resource_object, language):
    resource_folder_files = [file for file in os.listdir(resource_folder_path)]

    if "image.jpg" in resource_folder_files:
        file_size = os.path.getsize( os.path.join(resource_folder_path, "image.jpg") )

        file_info = resource_file_info.ResourceFileInfo()
        file_info.file_name = "image.jpg"
        file_info.file_size = file_size

        resource_object.params = {"alpha": "alpha.jpg" in resource_folder_files}
        resource_object.file_infos = [file_info]
        resource_object.type = resource_types.IMAGE

    if "ru.jpg" in resource_folder_files:
        file_name = language + ".jpg"
        file_size = os.path.getsize( os.path.join(resource_folder_path, file_name) )

        resource_object.file_infos = []

        file_info = resource_file_info.ResourceFileInfo()
        file_info.file_name = file_name
        file_info.file_size = file_size
        resource_object.file_infos.append(file_info)

        alpha_file_name = language + "_alpha.jpg"
        if alpha_file_name in resource_folder_files:
            alpha_file_size = os.path.getsize( os.path.join(resource_folder_path, alpha_file_name) )

            file_info = resource_file_info.ResourceFileInfo()
            file_info.file_name = alpha_file_name
            file_info.file_size = alpha_file_size
            resource_object.file_infos.append(file_info)
        resource_object.type = resource_types.LOCALIZED_IMAGE

    if "map.xml" in resource_folder_files:
        resource_name = "map.xml"
        file_path = os.path.join(resource_folder_path, resource_name)

        map_xml = create_empty_resource_info(resource_name, file_path)
        map_proplibs_xml = create_empty_resource_info(resource_name, file_path)

        resource_object.file_infos = [map_xml, map_proplibs_xml]
        resource_object.type = resource_types.MAP

    if "library.swf" in resource_folder_files:
        set_default_params(resource_object, "library.swf", resource_folder_path, resource_types.SWF_LIBRARY)

    if "object.3ds" in resource_folder_files:
        set_default_params(resource_object, "object.3ds", resource_folder_path, resource_types.TANKS_3DS_RESOURCE)

    if "localized.data_ru" in resource_folder_files:
        file_name = "localized.data_" + language
        set_default_params(resource_object, file_name, resource_folder_path, resource_types.LOCALIZATION)

    if "library.tara" in resource_folder_files:
        set_default_params(resource_object, "library.tara", resource_folder_path, resource_types.PROP_LIB)

    if "sound.swf" in resource_folder_files:
        set_default_params(resource_object, "sound.swf", resource_folder_path, resource_types.SOUND)

    if "image.tara" in resource_folder_files:
        set_default_params(resource_object, "image.tara", resource_folder_path, resource_types.MULTIFRAME_IMAGE)

def get_largest_version_from_resource_folder(resource_path):
    versions = [int(folder) for folder in os.listdir(resource_path) if not os.path.isfile(os.path.join(resource_path, folder))]
    versions.sort()
    return versions[-1]

def set_resource_params_from_dictionary(resource_dictionary, resource_object):
    resource_object.is_lazy = resource_dictionary["is_lazy"]

    if "hash_calculation_method_id" in resource_dictionary:
        resource_object.hash_calculation_method_id = resource_dictionary["version"]
    if "locales" in resource_dictionary:
        resource_object.locales = resource_dictionary["locales"]
    if "file_infos" in resource_dictionary:
        resource_object.file_infos = resource_dictionary["file_infos"]
    if "params" in resource_dictionary:
        resource_object.params = resource_dictionary["params"]

def get_resource_object(resource_folder_path, version, language):
    global resource_object_by_path_version_and_language

    resource_folder_path_without_base_dir = (resource_folder_path[len(RESOURCES_PATH)-1:]).replace("\\", "/")

    key = (resource_folder_path_without_base_dir, version, language)

    # if resource is already loaded then just return it
    if key in resource_object_by_path_version_and_language:
        return resource_object_by_path_version_and_language[key]

    resource_version = get_largest_version_from_resource_folder(resource_folder_path)
    resource_folder_path_with_version = os.path.join(resource_folder_path, str(resource_version))

    resource_object = resource_dispatcher_item.ResourceDispatcherItem()
    resource_object.id      = path_to_id[resource_folder_path_without_base_dir]
    resource_object.version = resource_version
    resource_object.item_type = "resource"

    resource_json_path = os.path.join(resource_folder_path_with_version, "resource_info.json")
    resource_dictionary = json_loader.cache_json_read(resource_json_path)

    set_params_from_resource_files(resource_folder_path_with_version, resource_object, language)
    set_resource_params_from_dictionary(resource_dictionary, resource_object)

    resource_object_by_path_version_and_language[(resource_folder_path, version, language)] = resource_object

    return resource_object
