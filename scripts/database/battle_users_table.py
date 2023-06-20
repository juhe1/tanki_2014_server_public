from global_models.battle.common.tank_global_model.team import Team
from . import database

def add_user(user_info, team, battle_id):
    user_info_tuple = (
        user_info.user_id,
        user_info.deaths,
        user_info.kills,
        user_info.score,
        int(team),
        battle_id,
        user_info.suspicious,
        user_info.uid,
        user_info.rank
    )

    connection = database.Connection()
    connection.cursor.execute("INSERT INTO BattleUsers (user_id, deaths, kills, score, team, battle_id, suspicious, uid, _rank) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", user_info_tuple)
    connection.connection.commit()
    connection.close()

def delete_user(user_id):
    query = "DELETE FROM BattleUsers WHERE user_id=(%s);"

    connection = database.Connection()
    connection.cursor.execute(query, (user_id,))
    connection.connection.commit()
    connection.close()

def get_users_by_battle_id(battle_id):
    query = "SELECT * FROM BattleUsers WHERE battle_id=(%s);"

    connection = database.Connection(dictionary=True)
    connection.cursor.execute(query, (battle_id,))
    rows = connection.cursor.fetchall()
    connection.close()

    return rows

def swap_teams(battle_id):
    query = "UPDATE BattleUsers SET team = (%s) WHERE team=(%s);"

    connection = database.Connection()

    connection.cursor.execute(query, (int(Team.BLUE), int(Team.RED)))
    connection.cursor.execute(query, (int(Team.RED), int(Team.BLUE)))

    connection.connection.commit()
    connection.close()

def set_deaths(deaths, user_id):
    query = ("UPDATE BattleUsers "
             "SET deaths = (%s) "
             "WHERE user_id = (%s);")
    data = (deaths, user_id)

    connection = database.Connection()
    connection.cursor.execute(query, data)
    connection.connection.commit()
    connection.close()

def set_kills(kills, user_id):
    query = ("UPDATE BattleUsers "
             "SET kills = (%s) "
             "WHERE user_id = (%s);")
    data = (kills, user_id)

    connection = database.Connection()
    connection.cursor.execute(query, data)
    connection.connection.commit()
    connection.close()

def set_score(score, user_id):
    query = ("UPDATE BattleUsers "
             "SET score = (%s) "
             "WHERE user_id = (%s);")
    data = (score, user_id)

    connection = database.Connection()
    connection.cursor.execute(query, data)
    connection.connection.commit()
    connection.close()

def set_team(team, user_id):
    query = ("UPDATE BattleUsers "
             "SET team = (%s) "
             "WHERE user_id = (%s);")
    data = (team, user_id)

    connection = database.Connection()
    connection.cursor.execute(query, data)
    connection.connection.commit()
    connection.close()

def set_suspicious(suspicious, user_id):
    query = ("UPDATE BattleUsers "
             "SET suspicious = (%s) "
             "WHERE user_id = (%s);")
    data = (suspicious, user_id)

    connection = database.Connection()
    connection.cursor.execute(query, data)
    connection.connection.commit()
    connection.close()

def set_rank(rank, user_id):
    query = ("UPDATE BattleUsers "
             "SET _rank = (%s) "
             "WHERE user_id = (%s);")
    data = (rank, user_id)

    connection = database.Connection()
    connection.cursor.execute(query, data)
    connection.connection.commit()
    connection.close()
