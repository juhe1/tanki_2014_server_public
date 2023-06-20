from global_models.battle.common.tank_global_model.team import Team
from rtree import index

# maximum count of mine positions that can be returned from mines inside bound
RESULT_COUNT = 20

class MineRTree:
    def __init__(self):
        rtree_properties = index.Property()
        rtree_properties.dimension = 3

        self.rtree_team1 = index.Index(properties=rtree_properties)
        self.rtree_team2 = index.Index(properties=rtree_properties)

    def get_rtree_by_team(self, team):
        match team:
            case Team.RED:
                return self.rtree_team1
            case Team.BLUE:
                return self.rtree_team2
            case Team.NONE:
                return self.rtree_team1

    def add_mine(self, mine):
        self.get_rtree_by_team(mine.team).insert(mine.mine_id, (mine.position.x, mine.position.y, mine.position.z, mine.position.x, mine.position.y, mine.position.z))

    def remove_mine(self, mine):
        self.get_rtree_by_team(mine.team).delete(mine.mine_id, (mine.position.x, mine.position.y, mine.position.z, mine.position.x, mine.position.y, mine.position.z))

    # this function will make bound_min xyz values to be lower than bound_max xyz values
    def correct_bounds(self, bound_min, bound_max):
        if bound_min.x > bound_max.x:
            bound_min.x = -bound_min.x
            bound_max.x = -bound_max.x

        if bound_min.y > bound_max.y:
            bound_min.y = -bound_min.y
            bound_max.y = -bound_max.y

        if bound_min.z > bound_max.z:
            bound_min.z = -bound_min.z
            bound_max.z = -bound_max.z

    def get_mine_ids_inside_bound(self, bound_min, bound_max, bound_pos, team):
        self.correct_bounds(bound_min, bound_max)

        mines = []

        for mine_id in [_id for _id in self.get_rtree_by_team(team).intersection((bound_min.x, bound_min.y, bound_min.z, bound_max.x, bound_max.y, bound_max.z))]:
            mines.append(mine_id)

        return mines
