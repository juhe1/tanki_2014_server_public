from client.layouts.entrance.models.login_model import login_model
from utils.binary.codecs import basic_codecs
from database import user_propertyes_table
from database import garage_tables
from database import users_table
import server_properties

import datetime
import bcrypt
import re

class RegistrationModelCommandHandler:
    def __init__(self, registration_model):
        client_object = registration_model.client_object
        self.registration_model_commands = registration_model.commands
        self.login_model = client_object.client_space_registry.get_model(space_name="entrance", game_object_name="entrance", model=login_model.LoginModel)

        self.CHECK_UID_COMMAND_ID = 300020060
        self.REGISTER_COMMAND_ID = 300020061

    def handle_command(self, binary_data, command_id):
        if command_id == self.CHECK_UID_COMMAND_ID:
            self.check_uid(binary_data)
            return True

        if command_id == self.REGISTER_COMMAND_ID:
            self.register(binary_data)
            return True

        return False

    def check_uid(self, binary_data):
        username = basic_codecs.StringCodec.decode(binary_data)
        if users_table.user_exist(username):
            self.registration_model_commands.entered_uid_is_incorrect()
        else:
            self.registration_model_commands.entered_uid_is_free()

    def register(self, binary_data):
        username = basic_codecs.StringCodec.decode(binary_data)
        password = basic_codecs.StringCodec.decode(binary_data)
        registered_url_code = basic_codecs.StringCodec.decode(binary_data)
        remember_me = basic_codecs.BooleanCodec.decode(binary_data)
        referral_hash_code = basic_codecs.OptionalCodec.decode((binary_data,), binary_data, basic_codecs.StringCodec)
        real_name = basic_codecs.StringCodec.decode(binary_data)
        id_number = basic_codecs.StringCodec.decode(binary_data)

        username_pattern = re.compile("^[a-zA-Z0-9_]{1,20}$") # TODO: test lenght 1 username in the game, because it can look weird
        password_pattern = re.compile("^.{1,50}$")

        if not username_pattern.match(username) or not password_pattern.match(password):
            return
        if users_table.user_exist(username):
            return

        reg_date = datetime.datetime.now()
        hashed_pasword = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        users_table.create_new_user({"name":username, "password":hashed_pasword, "email":"", "reg_date":reg_date})

        user_id = users_table.get_atribute_by_username(username, "id")
        user_propertyes = {"id":user_id, "crystals":server_properties.STARTING_CRYSTALS, "score":server_properties.STARTING_SCORE,
                           "last_visit":reg_date, "next_crystal_reward":reg_date, "user_roles":'[0]'}

        user_propertyes_table.create_new_user_property(user_propertyes)
        garage_tables.create_mounted_items_row(user_id)
        self.login_model.login(username)
