import server_properties

from mysql.connector import pooling
import mysql.connector

connection_pool = None

class Connection:
    def __init__(self, dictionary=False):
        self.connection_pool = connection_pool
        self.connection = connection_pool.get_connection()
        self.cursor = self.connection.cursor(dictionary=dictionary)

    def get_cursor(self):
        return self.cursor

    def close(self):
        self.cursor.close()
        self.connection.close()

def connect_to_database():
    global connection_pool

    # Create a connection pool
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        pool_name="mypool",
        pool_size=server_properties.DATABASE_CONNECTION_POOL_SIZE,
        host=server_properties.DATABASE_ADDRES,
        user=server_properties.DATABASE_USER,
        password=server_properties.DATABASE_PASSWORD,
        database=server_properties.DATABASE_NAME
    )

def create_users_table(cursor):
    users_query = (
        "CREATE TABLE Users ("
        "id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY, "
        "username VARCHAR(20), "
        "password BINARY(60), "
        "email VARCHAR(60), "
        "reg_date datetime)"
    )
    cursor.execute(users_query)

def create_user_properties_table(cursor):
    users_propertys_query = (
        "CREATE TABLE UserProperties ("
        "id INT(6) UNSIGNED PRIMARY KEY,"
        "crystals INT(4),"
        "score INT(4),"
        "last_visit datetime,"
        "next_crystal_reward datetime,"
        "user_roles JSON)"
    )
    cursor.execute(users_propertys_query)

def create_user_items_table(cursor):
    user_items_query = (
        "CREATE TABLE UserItems ("
        "user_id INT(6) UNSIGNED NOT NULL,"
        "item_id INT(4) UNSIGNED NOT NULL,"
        "upgrading_property_id TINYINT UNSIGNED,"
        "upgrade_done_time datetime DEFAULT NULL,"
        "property_levels_id BIGINT UNSIGNED,"
        "count INT(4),"
        "temporary_item_expiration datetime DEFAULT NULL)"
    )
    cursor.execute(user_items_query)

def create_property_table_table(cursor):
    property_levels_query = (
        "CREATE TABLE PropertyLevels ("
        "id BIGINT UNSIGNED NOT NULL,"
        "property_id TINYINT NOT NULL,"
        "property_level SMALLINT NOT NULL)"
    )
    cursor.execute(property_levels_query)

def create_mounted_table(cursor):
    mounted_items_query = (
        "CREATE TABLE MountedItems ("
        "user_id INT(6) UNSIGNED PRIMARY KEY NOT NULL,"
        "weapon_slot INT(4) UNSIGNED,"
        "armor_slot INT(4) UNSIGNED,"
        "color_slot INT(4) UNSIGNED)"
    )
    cursor.execute(mounted_items_query)

def create_battle_table(cursor):
    battle_query = (
        "CREATE TABLE Battles ("
        "battle_id INT(4) UNSIGNED PRIMARY KEY NOT NULL,"
        "auto_balance BOOL,"
        "battle_mode INT(1) UNSIGNED,"
        "friendly_fire BOOL,"
        "score_limit INT(4) UNSIGNED,"
        "time_limit_in_sec INT(4) UNSIGNED,"
        "battle_start_time datetime,"
        "fund INT(4) UNSIGNED,"
        "score_team1 INT(4) UNSIGNED,"
        "score_team2 INT(4) UNSIGNED,"
        "map_id INT(4) UNSIGNED,"
        "max_people_count INT(1) UNSIGNED,"
        "name VARCHAR(30),"
        "private_battle BOOL,"
        "pro_battle BOOL,"
        "rank_range_min INT(1) UNSIGNED,"
        "rank_range_max INT(1) UNSIGNED,"
        "theme INT(1) UNSIGNED,"
        "without_bonuses BOOL,"
        "without_crystals BOOL,"
        "without_supplies BOOL,"
        "without_upgrades BOOL)"
    )
    cursor.execute(battle_query)

def create_battle_users_table(cursor):
    battle_user_query = (
        "CREATE TABLE BattleUsers ("
        "user_id INT(8) UNSIGNED PRIMARY KEY NOT NULL,"
        "deaths INT(4) UNSIGNED,"
        "kills INT(4) UNSIGNED,"
        "score INT(4) UNSIGNED,"
        "team INT(1) UNSIGNED,"
        "battle_id INT(4) UNSIGNED,"
        "suspicious BOOL,"
        "uid VARCHAR(20),"
        "_rank INT(1) UNSIGNED)"
    )
    cursor.execute(battle_user_query)

def create_data_base():
    connection = mysql.connector.connect(
      host=server_properties.DATABASE_ADDRES,
      user=server_properties.DATABASE_USER,
      password=server_properties.DATABASE_PASSWORD
    )
    cursor = connection.cursor()

    cursor.execute("CREATE DATABASE " + server_properties.DATABASE_NAME)
    connection.commit()
    cursor.execute("USE " + server_properties.DATABASE_NAME)

    create_users_table(cursor)
    create_user_properties_table(cursor)
    create_user_items_table(cursor)
    create_property_table_table(cursor)
    create_mounted_table(cursor)
    create_battle_table(cursor)
    create_battle_users_table(cursor)
    connection.commit()

#create_data_base()
