from space import global_space

spaces_by_name = {}
spaces_by_id = {}

def add_space(id, name):
    global spaces_by_name, spaces_by_id

    new_global_space = global_space.GlobalSpace(id, name)
    spaces_by_name[name] = new_global_space
    spaces_by_id[id] = new_global_space
    return new_global_space

def remove_global_space_from_vars(global_space):
    spaces_by_name.pop(global_space.name)
    spaces_by_id.pop(global_space.id)

def get_all_spaces():
    global spaces_by_name
    return spaces_by_name.values()

def get_space_by_name(name):
    global spaces_by_name
    return spaces_by_name[name]

def get_space_by_id(id):
    global spaces_by_id
    return spaces_by_id[id]

def get_global_model(model, global_game_object_id=None, global_game_object_name=None, global_space_id=None, global_space_name=None):
    if global_space_id:
        global_space = get_space_by_id(global_space_id)
    else:
        global_space = get_space_by_name(global_space_name)

    if global_space == None:
        return

    return global_space.get_global_model(model, global_game_object_id, global_game_object_name)
