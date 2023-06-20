from . import database

import datetime

def add_new_battle(battle_data):
    battle_start_time = datetime.datetime.now()
    fund = 0
    score_team1 = 0
    score_team2 = 0

    # TODO: update fund, team scores and battle_start_time when they changes

    battle_data_tuple = (
        battle_data.battle_id,
        battle_data.auto_balance,
        int(battle_data.battle_mode),
        battle_data.friendly_fire,
        battle_data.limits.score_limit,
        battle_data.limits.time_limit_in_sec,
        battle_start_time,
        fund,
        score_team1,
        score_team2,
        battle_data.map_id,
        battle_data.max_people_count,
        battle_data.name,
        battle_data.private_battle,
        battle_data.pro_battle,
        battle_data.rank_range.min,
        battle_data.rank_range.max,
        int(battle_data.theme),
        battle_data.without_bonuses,
        battle_data.without_crystals,
        battle_data.without_supplies,
        battle_data.without_upgrades
    )

    connection = database.Connection()
    connection.cursor.execute("INSERT INTO Battles (battle_id, auto_balance, battle_mode, friendly_fire, score_limit, time_limit_in_sec, battle_start_time, fund, score_team1, score_team2, map_id, max_people_count, name, private_battle, pro_battle, rank_range_min, rank_range_max, theme, without_bonuses, without_crystals, without_supplies, without_upgrades) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", battle_data_tuple)
    connection.connection.commit()
    connection.close()

def delete_battle(battle_id):
    query = "DELETE FROM Battles WHERE battle_id=(%s);"

    connection = database.Connection()
    connection.cursor.execute(query, (battle_id,))
    connection.connection.commit()
    connection.close()

def get_highest_battle_id():
    query = "SELECT MAX(battle_id) FROM Battles;"

    connection = database.Connection()
    connection.cursor.execute(query)
    rows = connection.cursor.fetchall()
    connection.close()

    if len(rows) == 0 or rows[0][0] == None:
        return 0

    return rows[0][0]

def get_all_battle_rows():
    query = "SELECT * FROM Battles;"

    connection = database.Connection(dictionary=True)
    connection.cursor.execute(query)
    rows = connection.cursor.fetchall()
    connection.close()

    return rows

def set_fund(fund, battle_id):
    query = ("UPDATE Battles "
             "SET fund = (%s) "
             "WHERE battle_id = (%s);")
    data = (fund, battle_id)

    connection = database.Connection()
    connection.cursor.execute(query, data)
    connection.connection.commit()
    connection.close()

def set_score_team1(score, battle_id):
    query = ("UPDATE Battles "
             "SET score_team1 = (%s) "
             "WHERE battle_id = (%s);")
    data = (score, battle_id)

    connection = database.Connection()
    connection.cursor.execute(query, data)
    connection.connection.commit()
    connection.close()

def set_score_team2(score, battle_id):
    query = ("UPDATE Battles "
             "SET score_team2 = (%s) "
             "WHERE battle_id = (%s);")
    data = (score, battle_id)

    connection = database.Connection()
    connection.cursor.execute(query, data)
    connection.connection.commit()
    connection.close()

def set_battle_start_time(battle_start_time, battle_id):
    query = ("UPDATE Battles "
             "SET battle_start_time = (%s) "
             "WHERE battle_id = (%s);")
    data = (battle_start_time, battle_id)

    connection = database.Connection()
    connection.cursor.execute(query, data)
    connection.connection.commit()
    connection.close()
