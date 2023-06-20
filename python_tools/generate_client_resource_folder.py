import version_and_id_to_path
from xml.dom import minidom
import shutil
import glob
import json
import os

WINDOWS_CACHE_PATH  = r"C:\Users\juho1\AppData\Local\Microsoft\Windows\INetCache\IE"
SERVER_RESOURCE_FOLDER_PATH = "D:\\juho1\\tankkin_modaus\\tanki_online\\2014_tanki_backup\\server_v2\\client_resources\\"
CLIENT_RESOURCE_FOLDER_PATH = "D:\\juho1\\tankkin_modaus\\tanki_online\\2014_tanki_backup\\client\\resources\\"
SERVER_CONFIG_FOLDER = "D:\\juho1\\tankkin_modaus\\tanki_online\\2014_tanki_backup\\server_v2\\configs\\"

_id = 0
path_to_id = {}

# list all folders that doesn't have folder in it
def list_folderless_folders(dir):
    return [root for root, dirs, files in os.walk(dir) if dirs == []]
   
def create_resource_folder(resource_version, resource_folder_path):
    resource_new_path = version_and_id_to_path.version_id_to_path(_id, resource_version)
    resource_new_path = os.path.join(CLIENT_RESOURCE_FOLDER_PATH, resource_new_path)
    
    # remove the destination directory
    if os.path.exists(resource_new_path):
        shutil.rmtree(resource_new_path)
    
    # create new folder for resources
    if not os.path.exists(resource_new_path):
        os.makedirs(resource_new_path)
    
    # copy all content from folder to new path
    for file_name in os.listdir(resource_folder_path):
        destination = os.path.join(resource_new_path, file_name)
        source = os.path.join(resource_folder_path, file_name)
        shutil.copy(source, destination)
    
def generate_client_resources(path):
    global _id, path_to_id
    resource_folders = list_folderless_folders(path)

    for resource_folder_path in resource_folders:
        resource_folder_path_without_base_dir_and_version = os.path.split( resource_folder_path[len(SERVER_RESOURCE_FOLDER_PATH)-1:].replace("\\", "/") )[0]
        if not resource_folder_path_without_base_dir_and_version in path_to_id:
            _id += 1
            path_to_id[resource_folder_path_without_base_dir_and_version] = _id
            
        resource_folder_name = os.path.basename(resource_folder_path)
        create_resource_folder(int(resource_folder_name), resource_folder_path)
    
def edit_proplib_xml(path):
    dom = minidom.parse(path)
    proplib_elements = dom.getElementsByTagName('library')
    for proplib_element in proplib_elements:
        resource_path = proplib_element.attributes['resource-id'].value
        proplib_element.attributes['resource-id'].value = hex(path_to_id[resource_path])[2:]
        
    with open( path, "w" ) as fs: 
        fs.write( dom.toxml() )
        fs.close()
  
    
# for example this function will rename resource id from proplib.xml file. example: ("battle/proplibs/Tiles" --> "e552f34")
def rename_resource_ids_from_xmls():
    file_paths = [os.path.join(root, name) for root, dirs, files in os.walk(CLIENT_RESOURCE_FOLDER_PATH) for name in files]
    for file_path in file_paths:
        file_name = os.path.split(file_path)[1]
        if file_name == "proplibs.xml":
            edit_proplib_xml(file_path)

def empty_windows_cache():
    file_paths = [os.path.join(root, name) for root, dirs, files in os.walk(WINDOWS_CACHE_PATH) for name in files]
    for file_path in file_paths:
        os.remove(file_path)

def main():
    empty_windows_cache()
    generate_client_resources(SERVER_RESOURCE_FOLDER_PATH)
    rename_resource_ids_from_xmls()

    # save path to id
    json_file_path = os.path.join(SERVER_CONFIG_FOLDER, "path_to_id.json")
    with open(json_file_path, "w") as file:
        json.dump(path_to_id, file)
        
main()