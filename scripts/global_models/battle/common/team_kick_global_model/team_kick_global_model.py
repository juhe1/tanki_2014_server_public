from client.layouts.battle.models.team_kick_model import team_kick_model
from global_models.battle.common.tank_global_model.team import Team
from space.global_model import GlobalModel
from . import team_kick_model_cc
from . import user_team_kick_data
import server_properties

class TeamKickGlobalModel(GlobalModel):

    CLIENT_MODEL = team_kick_model.TeamKickModel

    def __init__(self, global_game_object, global_space, owner_id=None):
        super().__init__(global_game_object, global_space, owner_id)

        self.team_kick_model_cc = self.create_cc()
        self.blue_user_team_kick_data_by_user_id = {}
        self.red_user_team_kick_data_by_user_id = {}
        self.votes_by_user_id = {}
        self.user_votes_by_user_id = {} # example: {<vooooter_user_id>:[<voted_user1>, <voted_user2>...]}

    def add_user(self, user_id, team, excluded):
        _user_team_kick_data = user_team_kick_data.UserTeamKickData()
        _user_team_kick_data.excluded = excluded
        _user_team_kick_data.user_id = user_id

        if team == Team.BLUE:
            data_list = self.blue_user_team_kick_data_by_user_id
        else:
            data_list = self.red_user_team_kick_data_by_user_id

        self.votes_by_user_id[user_id] = 0
        self.user_votes_by_user_id[user_id] = []
        data_list[user_id] = _user_team_kick_data
        self.broadcast_command("user_connected", (_user_team_kick_data,))
        self.broadcast_command("allow_voting", (user_id, 0))

    def remove_user(self, user_id):
        if user_id in self.blue_user_team_kick_data_by_user_id:
            self.blue_user_team_kick_data_by_user_id.pop(user_id)
            return

        # remove disconnecting user votes
        for voted_id in user_votes_by_user_id[user_id]:
            self.add_votes(voted_id, -1)

        self.votes_by_user_id.pop(user_id)
        self.user_votes_by_user_id.pop(user_id)
        self.red_user_team_kick_data_by_user_id.pop(user_id)
        self.broadcast_command("user_disconnect", (user_id,))

    def get_all_votable_user_ids_by_user_id(self, user_id):
        return [_user_team_kick_data.user_id for _user_team_kick_data in self.get_user_team_kick_data_list_by_user_id(user_id) if not _user_team_kick_data.excluded]

    def get_user_team_kick_data_by_user_id(self, user_id):
        return self.get_user_team_kick_data_dictionary_by_user_id(user_id)[user_id]

    def vote(self, voter_id, voted_id):
        if not voted_id in self.votes_by_user_id: return
        if not voter_id in self.user_votes_by_user_id: return
        if self.get_user_team_kick_data_by_user_id(voted_id).excluded: return

        self.user_votes_by_user_id[voter_id].append(voted_id)
        self.add_votes(voted_id)

    def add_votes(self, user_id, count=1):
        self.votes_by_user_id[user_id] += count
        self.broadcast_command("update_votes", (user_id, self.votes_by_user_id[user_id]))

    def get_user_team_kick_data_list_by_user_id(self, user_id):
        return list(self.get_user_team_kick_data_dictionary_by_user_id(user_id).values())

    def get_user_team_kick_data_dictionary_by_user_id(self, user_id):
        if user_id in self.blue_user_team_kick_data_by_user_id:
            return self.blue_user_team_kick_data_by_user_id

        return self.red_user_team_kick_data_by_user_id

    def create_cc(self):
        cc = team_kick_model_cc.TeamKickModelCC()
        cc.disabled = False
        cc.duration_immunity_affter_enter_in_sec = server_properties.TEAM_KICK_DURATION_IMMUNITY_AFFTER_ENTER_IN_SEC
        cc.enter_time_diff_in_sec = 0
        cc.immunity_stay_in_battle_in_sec = server_properties.TEAM_KICK_IMMUNITY_STAY_IN_BATTLE_IN_SEC
        return cc

    def get_model_data(self, user_id):
        team_specifig_user_team_kick_data = self.get_user_team_kick_data_dictionary_by_user_id(user_id)
        self.team_kick_model_cc.allys = list(team_specifig_user_team_kick_data.values())
        self.team_kick_model_cc.current_user = team_specifig_user_team_kick_data[user_id]
        self.team_kick_model_cc.allys.remove(self.team_kick_model_cc.current_user)
        return self.team_kick_model_cc
