from . import team_kick_model_command_handler
from . import team_kick_model_commands
from . import team_kick_model_data
from client.space.model import Model

class TeamKickModel(Model):
    model_id = 300080038

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        team_kick_model_cc = global_model.get_model_data(self.client_object.user_id)

        self.model_data = team_kick_model_data.TeamKickModelData(team_kick_model_cc)
        self.commands = team_kick_model_commands.TeamKickModelCommands(client_space, game_object)
        self.command_handler = team_kick_model_command_handler.TeamKickModelCommandHandler(self)

        self.voted_users = []

    def loaded_from_client(self):
        self.allow_client_to_vote()

    def vote(self, voted_id):
        if voted_id in self.voted_users: return
        self.voted_users.append(voted_id)

        self.global_model.vote(self.client_object.user_id, voted_id)

    def allow_client_to_vote(self):
        user_ids = self.global_model.get_all_votable_user_ids_by_user_id(self.client_object.user_id)
        for user_id in user_ids:
            if user_id == self.client_object.user_id: continue
            self.commands.allow_voting(user_id, self.global_model.votes_by_user_id[user_id])
