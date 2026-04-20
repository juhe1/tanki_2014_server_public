# Tanki 2014 server
This is server for the original tanki online client from 2014. I don't anymore develop it, so I decided to make it public. This server is not finished there is a lot of missing features.

I suggest using this code only as a documentation, because the code is not robust for real use. It has lot of bugs, doesn't have proper thread safety and also performance is poor. Also the architecture of the server is not ideal. If I would write it again, I would get rid of the client specifig spaces and I would make every space behave like global spaces.

## Get the server up and running quickly
Follow these steps if you want to get the server running quickly. You can ignore the "Manual setup" section, if you follow these.

## Manual setup
Use python 3.10.0, newer versions can cause `RuntimeError: can't create new thread at interpreter shutdown` error.

Intall requirments using the command ```pip install -r requirements.txt```. Consider setting up fresh venv before installing, because the requirments contain specifig version of certain packages and they may collide with already installed packets.

~~You can generate the database by uncommenting line `#create_data_base()` from scripts/database/database.py. Remember to recomment it after running the server.~~

Resources can be found inside client_resources.7z. Unzip them and after that you should run `python_tools/generate_client_resource_folder.py` script. Change the SERVER_RESOURCE_FOLDER_PATH, CLIENT_RESOURCE_FOLDER_PATH, SERVER_CONFIG_FOLDER and WINDOWS_CACHE_PATH variables from the script before running it. The CLIENT_RESOURCE_FOLDER_PATH should point to the resources folder that is inside the folder that contains the client files. You can get the client from releases.

Setup mysql database. I am using version 8.0.31. You should change DATABASE_USER and DATABASE_PASSWORD from scripts/server_properties.py.

Now if you run the game server and the http server from client folder, you can connect.