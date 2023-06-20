from client.dispatcher.dispatcher_model import model_data
from client.layouts.lobby.lobby_enums import UserRole
from utils.binary.codecs import basic_codecs
from database import user_propertyes_table
from utils.binary import binary_buffer
from . import user_property_model
from database import users_table
from client import ranks

import datetime
import json

VOTE_IMMUNITE_ROLES = [UserRole.ADMIN]

class UserPropertyModelData:
    def __init__(self, game_object, client_object, username):
        self.game_object = game_object

        client_database_id = users_table.get_atribute_by_username(username, "id")
        score = user_propertyes_table.get_atribute_by_id(client_database_id, "score")
        current_rank_index = ranks.get_rank_id_by_score(score)
        last_visit = user_propertyes_table.get_atribute_by_id(client_database_id, "last_visit")
        registratio_date = users_table.get_atribute_by_username(username, "reg_date")
        datetime_now = datetime.datetime.now()

        email = users_table.get_atribute_by_username(username, "email")
        if email == "": email = None

        self.crystals = user_propertyes_table.get_atribute_by_id(client_database_id, "crystals")
        self.current_rank_score = ranks.ranks[current_rank_index]["score"]
        self.days_from_last_visit = (datetime_now - last_visit).days
        self.days_from_registration = (datetime_now - registratio_date).days
        self.duration_crystal_abonement = 45
        self.game_host = "tankionline.com"
        self.has_double_crystal = False
        self.next_rank_score = ranks.ranks[current_rank_index + 1]["score"]
        self.place = 0
        self.rank = current_rank_index + 1
        self.rating = 0.0
        self.score = user_propertyes_table.get_atribute_by_id(client_database_id, "score")
        self.server_number = 1
        self.template_battle_page = "battles"
        self.uid = username
        self.user_id = client_database_id

        user_roles = json.loads(user_propertyes_table.get_atribute_by_id(client_database_id, "user_roles"))
        self.user_roles = self.role_ids_to_enums(user_roles)

        self.email = email

        client_object.username = self.uid
        client_object.user_id = self.user_id


    def role_ids_to_enums(self, role_ids):
        roles = []
        for role_id in role_ids:
            if role_id == 0:
                roles.append(UserRole.NORMAL)
            if role_id == 1:
                roles.append(UserRole.ADMIN)
            if role_id == 2:
                roles.append(UserRole.SPECTATOR)
        return roles

    def user_owns_role(self, role_enum):
        return role_enum in self.user_roles

    def get_user_roles(self):
        return self.user_roles

    def has_vote_immunity(self):
        return any(item in self.user_roles for item in VOTE_IMMUNITE_ROLES)

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.IntCodec.encode(self.crystals, buffer)
        basic_codecs.IntCodec.encode(self.current_rank_score, buffer)
        basic_codecs.IntCodec.encode(self.days_from_last_visit, buffer)
        basic_codecs.IntCodec.encode(self.days_from_registration, buffer)
        basic_codecs.IntCodec.encode(self.duration_crystal_abonement, buffer)
        basic_codecs.StringCodec.encode(self.game_host, buffer)
        basic_codecs.BooleanCodec.encode(self.has_double_crystal, buffer)
        basic_codecs.LongCodec.encode(self.user_id, buffer)
        basic_codecs.IntCodec.encode(self.next_rank_score, buffer)
        basic_codecs.IntCodec.encode(self.place, buffer)
        basic_codecs.ByteCodec.encode(self.rank, buffer)
        basic_codecs.FloatCodec.encode(self.rating, buffer)
        basic_codecs.IntCodec.encode(self.score, buffer)
        basic_codecs.IntCodec.encode(self.server_number, buffer)
        basic_codecs.StringCodec.encode(self.template_battle_page, buffer)
        basic_codecs.StringCodec.encode(self.uid, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = self.game_object.get_model(user_property_model.UserPropertyModel).model_id
        return _model_data
