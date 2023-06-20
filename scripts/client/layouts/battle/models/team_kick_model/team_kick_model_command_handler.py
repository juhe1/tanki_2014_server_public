from utils.binary.codecs import basic_codecs

class TeamKickModelCommandHandler:
    def __init__(self, team_kick_model):
        self.team_kick_model = team_kick_model
        self.VOTE_COMMAND_ID = 300080019

    def handle_command(self, binary_data, command_id):
        if command_id == self.VOTE_COMMAND_ID:
            self.vote(binary_data)
            return True

    def vote(self, binary_data):
        voted_id = basic_codecs.LongCodec.decode(binary_data)
        self.team_kick_model.vote(voted_id)
