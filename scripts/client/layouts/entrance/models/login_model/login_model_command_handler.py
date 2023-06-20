from utils.binary.codecs import basic_codecs
from database import users_table

import bcrypt
import re

class LoginModelCommandHandler:
    def __init__(self, login_model):
        self.login_model = login_model
        self.login_model_commands = login_model.commands
        self.client_object = login_model.client_object
        self.LOGIN_COMMAND_ID = 300020048

    def handle_command(self, binary_data, command_id):
        if command_id == self.LOGIN_COMMAND_ID:
            self.login(binary_data)
            return True

    def login(self, binary_data):
        login_username_or_email = basic_codecs.StringCodec.decode(binary_data)
        login_password = basic_codecs.StringCodec.decode(binary_data)
        remember_me = basic_codecs.BooleanCodec.decode(binary_data)

        username_pattern = re.compile("^[a-zA-Z0-9_]{1,20}$")
        password_pattern = re.compile("^.{1,50}$")

        if not username_pattern.match(login_username_or_email) or not password_pattern.match(login_password):
            self.login_model_commands.wrong_password()
            return

        correct_password_hash = users_table.get_atribute_by_username(login_username_or_email, "password")
        if correct_password_hash == None: # if user doesnt exist
            self.login_model_commands.wrong_password()
            return

        if bcrypt.checkpw(login_password.encode("utf-8"), bytes(correct_password_hash)):
            print("user:", login_username_or_email, " successfully logged in!!!", "remember_me:", remember_me)
            self.login_model.login(login_username_or_email)
            return

        self.login_model_commands.wrong_password()
