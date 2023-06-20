import enum

class Layout(enum.Enum):
    BATTLE_SELECT = 1
    GARAGE = 2
    BATTLE = 3
    PAYMENT = 4
    RELOAD_SPACE = 5


class UserRole(enum.Enum):
    NORMAL = 1
    ADMIN = 2
    SPECTATOR = 3
