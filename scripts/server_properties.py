from client.layouts.battle_list.battle_data import battle_limits

IP = "127.0.0.1"
PORTS = [1212]
NGROK_SPACE_PORTS = [1213]
SPACE_IP = IP
SPACE_PORTS = [1213]
MAX_PLAYER_COUNT = 30
RECEIVE_BUFFER_SIZE = 1024 * 5
DEFAULT_CONFFIG_URL = "127.0.0.1:8000/config.xml"

DATABASE_ADDRES = "localhost"
DATABASE_USER = "root"
DATABASE_PASSWORD = "juho"
DATABASE_NAME = "tanki_2014_database"
DATABASE_CONNECTION_POOL_SIZE = 5

DISABLE_HEX_DUMP = True
DEBUG_ENABLED = False
PRINT_PACKAGES_ENABLED = False
GLOBAL_GAME_OBJECT_ID_OFFSET = 100000

CONFIG_DIRECTORY = "configs/"
GARAGE_ITEMS_FOLDER = CONFIG_DIRECTORY + "garage_items"
GRAPHICS_SETTINGS_FOLDER = CONFIG_DIRECTORY + "graphics_settings"

STARTING_CRYSTALS = 5000000
STARTING_SCORE = 0
STARTING_ITEM_IDS = [1, 5, 100]

DISABLE_PAYMENT = True # keep that true, because we dont have that feature on the server yet

# login propertys
IN_GAME_REGISTRATION = True # keep that true, because we dont have that feature on the server yet
ENABLE_REQUIRED_EMAIL = False # keep that false, because we dont have that feature on the server yet
MAX_PASSWORD_LENGTH = 50
MIN_PASSWORD_LENGTH = 6

# garage propertys
UPGRADE_SPEEDUP_COEFFICIENT = 50
ENABLE_UPGRADES = True # keep that true, because we dont have that feature on the server yet
FIRST_AID_ITEM_ID = 500
DOUBLE_ARMOR_ITEM_ID = 501
DOUBLE_POWER_ITEM_ID = 502
NITRO_ITEM_ID = 503
MINE_ITEM_ID = 504

# battle select propertys property
MAXIMUM_BATTLE_COUNT = 500
PRO_BATTLE_ENTER_PRICE = 500
DM_BATTLE_LIMIT = battle_limits.BattleLimits()
DM_BATTLE_LIMIT.score_limit = 900
DM_BATTLE_LIMIT.time_limit_in_sec = 900
TDM_BATTLE_LIMIT = battle_limits.BattleLimits()
TDM_BATTLE_LIMIT.score_limit = 901
TDM_BATTLE_LIMIT.time_limit_in_sec = 900
CTF_BATTLE_LIMIT = battle_limits.BattleLimits()
CTF_BATTLE_LIMIT.score_limit = 902
CTF_BATTLE_LIMIT.time_limit_in_sec = 900
CP_BATTLE_LIMIT = battle_limits.BattleLimits()
CP_BATTLE_LIMIT.score_limit = 903
CP_BATTLE_LIMIT.time_limit_in_sec = 900

# battle field propertys
TEAM_KICK_IMMUNITY_STAY_IN_BATTLE_IN_SEC = 1000
TEAM_KICK_DURATION_IMMUNITY_AFFTER_ENTER_IN_SEC = 1
COLOR_TRANSFORM_MULTIPLIER = 10.0
IDLE_KICK_PERIOD_MSEC = 60000 * 5
BONUS_FALL_SPEED = 0.3
BILLBOARD_IMAGE_RESOURCE = "/battle/images/bill_boards/default"
KILL_SCORE = 10
KILL_FUND = 1
PLACEHOLDER_TIME_IN_SEC = 60 * 3 # how long we keep place in battle for disconnected user
ROUND_END_SCREEN_TIME_IN_SEC = 10
SCORE_SAVE_INTERVAL = 50 # how many xp user need to earn until it is saved to database. this is made to reduce the load for database

GOLD_BOX_DROP_PROBABILITY = 1 # org: 7000
GOLD_NOTIFICATION_MESSAGE = "Gold box will be dropped soon! (tai jotenki nuin se muistaakseni meni)"
#GOLD_TAKEN_NOTIFICATION_MESSAGE = "jee! jee! jee!!! gold is TAKEN!!!!"
GOLD_DROP_TIME = 10 # org: 45
GOLD_BOX_REWARD = 1000

CRYSTAL_BOX_REWARD = 10
NUM_FUND_CHANGES_FOR_CRYSTAL_DROP = 1 # how many times fund need to be changed before crystal box will be dropped

BONUS_FALL_SPEED = 200
SUPPLIE_BOX_SPAWN_TIME_IN_SEC = 10
ARMOR_BOX_LIFE_TIME_IN_SEC = 60
CRYSTAL_BOX_LIFE_TIME_IN_SEC = 60 * 20
GOLD_BOX_LIFE_TIME_IN_SEC = 60 * 60 * 200
MED_BOX_LIFE_TIME_IN_SEC = 60 * 2
NOS_BOX_LIFE_TIME_IN_SEC = 60 * 2
POWER_BOX_LIFE_TIME_IN_SEC = 60 * 2

# tank propertys
TANK_ACTIVATION_DELAY_IN_MS = 3000
TANK_SPAWN_DELAY_IN_MS = 4000
TANK_DEAD_TIME_IN_MS = 3000
MIN_ALLOWED_Z = -2000
MAXIMUM_ALLOWED_TANK_POSITION_DIFFERENCE = 100 # how much target real position and the position that we get from client can be different
TEMPERATURE_UPDATE_DELAY = 0.5
TEMPERATURE_CHANGE_FACTOR = 5

# mine propertys
MINE_ACTIVATE_TIME_MS = 1000
MINE_FAR_VISIBILITY_RADIUS = 2300.0
MINE_IMPACT_FORCE = 2004.4
MINE_MIN_DISTANCE_FROM_BASE = 203.0 # this means basicaly the distance from flag pole
MINE_NEAR_VISIBLITY_RADIUS = 2463.0
MINE_RADIUS = 2463.0 # this is propably used in calculating the position where the mine drops

# supplie propertys
FIRST_AID_COOL_DOWN_TIME_IN_SEC = 75
DOUBLE_ARMOR_COOL_DOWN_TIME_IN_SEC = 75
DOUBLE_POWER_COOL_DOWN_TIME_IN_SEC = 75
NITRO_COOL_DOWN_TIME_IN_SEC = 75
MINE_COOL_DOWN_TIME_IN_SEC = 0
MINE_OFFSET_FROM_GROUND = 20

NITRO_SPEED_COEFFICIENT = 1.3

DOUBLE_ARMOR_EFFECT_TIME_IN_SEC = 60
DOUBLE_POWER_EFFECT_TIME_IN_SEC = 60
NITRO_EFFECT_TIME_IN_SEC = 60

FIRST_AID_EFFECT_TIME_IN_SEC = 40
FIRST_AID_HEAL_STEP_HP = 30
FIRST_AID_HEAL_STEPPING_SPEED_IN_SECONDS = 1
