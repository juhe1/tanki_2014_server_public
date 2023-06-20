from utils.binary.codecs import basic_codecs

class SettingsModelCommandHandler:
    def __init__(self, settings_model):
        self.settings_model = settings_model
        self.SHOW_SETTINGS_COMMAND_ID = 300050037

    def handle_command(self, binary_data, command_id):
        if command_id == self.SHOW_SETTINGS_COMMAND_ID:
            self.settings_model.commands.open_settings()
            return True
