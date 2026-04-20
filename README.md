# Tanki 2014 server
This is server for the original tanki online client from 2014. I don't anymore develop it, so I decided to make it public. This server is not finished there is a lot of missing features.

I suggest using the code only as a documentation, because the code is not robust for real use. It has lot of bugs, does't have proper thread safety and also performance is poor. The code that is in the repo is not in working state, you will need to remove/change some isida config, because that weapon was never finished. Also the architecture of the server is not ideal. If I would write it again, I would get rid of the local space and I would make every space behave like global spaces.

## Get the server up and running quickly
Follow these steps if you want to get the server running quickly. You can ignore the manual setup steps, if you follow these.

## Manual setup
Use python 3.10.0, never versions can cause `Exception in thread Thread-108 (recive_commands):` error.

You can generate the database by uncommenting line `#create_data_base()` from scripts/database/database.py. Remember to recomment it after running the server.

Resources can be found inside client_resources.7zip. Unzip them and after that you should run `python_tools/generate_client_resource_folder.py` script. Change the SERVER_RESOURCE_FOLDER_PATH, CLIENT_RESOURCE_FOLDER_PATH, SERVER_CONFIG_FOLDER and WINDOWS_CACHE_PATH variables from the script before running it. The CLIENT_RESOURCE_FOLDER_PATH should point to the resources folder that is inside the folder that contains the client files. You can get the client from releases.

Setup mysql database. I am using version 8.0.31. You should change DATABASE_USER and DATABASE_PASSWORD from scripts/server_properties.py.

Now if you run the server and http server, you can connect to it using the client.