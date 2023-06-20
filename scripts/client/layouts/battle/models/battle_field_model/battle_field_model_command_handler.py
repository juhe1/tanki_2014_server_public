from utils.binary.codecs import basic_codecs

class BattleFieldModelCommandHandler:
    def __init__(self):
        self.EXAMPLE_COMMAND_ID = 11111111111

    def handle_command(self, binary_data, command_id):
        if command_id == self.EXAMPLE_COMMAND_ID:
            pass
            return True
