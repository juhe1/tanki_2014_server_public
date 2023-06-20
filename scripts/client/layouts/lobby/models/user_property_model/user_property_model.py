from global_models.battle.common.battle_field_global_model import battle_field_global_model
from . import user_property_model_commands
from database import user_propertyes_table
from database import battle_users_table
from . import user_property_model_data
from client.space.model import Model
from database import garage_tables
from client import ranks
import server_properties

class UserPropertyModel(Model):
    model_id = 300050071

    def __init__(self, game_object, client_space, client_object, username, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.model_data = user_property_model_data.UserPropertyModelData(self.game_object, self.client_object, username)
        self.commands = user_property_model_commands.UserPropertyModelCommands(client_space, game_object)
        self.command_handler = None

        self.score_buffer = 0
        self.next_rank = ranks.get_rank_by_id(self.model_data.rank + 1) # next_rank is here, because we dont want to get next_rank every score update, because it adds load to server
        self.client_object.database_garage_item_loader.load_items(self.client_object.user_id)
        client_object.user_property_model = self

    def add_buffered_score(self, score):
        self.score_buffer += score

        score = self.model_data.score + self.score_buffer
        self.commands.update_score(score)
        self.check_for_rank_up(score)

        # update database and user_data every 50 score
        if self.score_buffer >= server_properties.SCORE_SAVE_INTERVAL:
            self.save_score_buffer()

    def add_score(self, score):
        self.model_data.score += score
        user_propertyes_table.set_score(self.model_data.score, self.client_object.user_id)
        self.commands.update_score(score)
        self.check_for_rank_up(self.model_data.score)

    def check_for_rank_up(self, score):
        if score < self.next_rank["score"]: return

        self.model_data.rank += 1
        self.next_rank = ranks.get_rank_by_id(self.model_data.rank + 1)
        new_rank = ranks.get_rank_by_id(self.model_data.rank)
        self.save_score_buffer()

        self.add_crystals(self.next_rank["reward"])
        self.commands.update_rank(self.model_data.rank, self.model_data.score, new_rank["score"], self.next_rank["score"], self.next_rank["reward"])

        # return if user is not in battle
        battle_global_space = self.client_object.current_battle_global_space
        if battle_global_space == None: return

        _battle_field_global_model = battle_global_space.get_global_model(battle_field_global_model.BattleFieldGlobalModel, global_game_object_name="default_game_object")
        _battle_field_global_model.rank_up(self.client_object.user_id, self.model_data.rank)

    def save_score_buffer(self):
        self.model_data.score += self.score_buffer
        user_propertyes_table.set_score(self.model_data.score, self.client_object.user_id)
        self.score_buffer = 0

    def subtract_crystals(self, crystal_count):
        if crystal_count < 0: return
        self.model_data.crystals -= crystal_count
        user_propertyes_table.set_crystal_count(self.model_data.crystals, self.client_object.user_id)

    def add_crystals(self, crystal_count):
        if crystal_count < 0: return
        self.model_data.crystals += crystal_count
        user_propertyes_table.set_crystal_count(self.model_data.crystals, self.client_object.user_id)
        self.commands.change_crystal(crystal_count)
