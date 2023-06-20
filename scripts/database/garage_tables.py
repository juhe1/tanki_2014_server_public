from client.layouts.garage.database import database_garage_item
from client.layouts.garage.garage_utils import name_to_id
from loaders.garage_item_loader import garage_item_loader
from utils.log import console_out

from database import database

import datetime

def create_mounted_items_row(user_id):
    query = ("INSERT INTO MountedItems (user_id, weapon_slot, armor_slot, color_slot)"
             "VALUES (%s, %s, %s, %s)")
    values = (user_id, None, None, None)
    connection = database.Connection()
    connection.cursor.execute(query, values)
    connection.connection.commit()
    connection.close()

def add_item(item, user_id):
    connection = database.Connection()
    connection.cursor.execute("SELECT MAX(id) FROM PropertyLevels;")
    last_id_rows = connection.cursor.fetchall()

    if not item.upgradable_property_data_levels == {}:
        item.property_levels_id = 1
        if last_id_rows[0][0]:
            item.property_levels_id = last_id_rows[0][0] + 1
            #                                      ----

    for property_id, property_level in item.upgradable_property_data_levels.items():
        property_data = (item.property_levels_id, property_id, property_level)
        query = ("INSERT INTO PropertyLevels (id, property_id, property_level)"
                 "VALUES (%s, %s, %s)")
        connection.cursor.execute(query, property_data)

    item_data = (user_id, item.item_id, item.upgrading_property_id, item.upgrade_done_time,
                 item.property_levels_id, item.count, item.temporary_item_expiration_time)
    query = ("INSERT INTO UserItems (user_id, item_id, upgrading_property_id, upgrade_done_time, property_levels_id, count, temporary_item_expiration)"
             "VALUES (%s, %s, %s, %s, %s, %s, %s)")
    connection.cursor.execute(query, item_data)
    connection.connection.commit()
    connection.close()

def edit_item(item, user_id):
    query = ("UPDATE UserItems "
             "SET upgrading_property_id = (%s), upgrade_done_time = (%s), property_levels_id = (%s), count = (%s), temporary_item_expiration = (%s) "
             "WHERE user_id = (%s) "
             "AND item_id = (%s);")
    data = (item.upgrading_property_id, item.upgrade_done_time, item.property_levels_id,
            item.count, item.temporary_item_expiration_time, user_id, item.item_id)

    connection = database.Connection()
    connection.cursor.execute(query, data)

    for upgradable_property_id, upgradable_property_value in item.upgradable_property_data_levels.items():
        query = ("UPDATE PropertyLevels "
                 "SET property_level = (%s) "
                 "WHERE id = (%s) "
                 "AND property_id = (%s);")
        data = (upgradable_property_value, item.property_levels_id, upgradable_property_id)
        connection.cursor.execute(query, data)

    connection.connection.commit()
    connection.close()

def mount_item(item, item_category, user_id):
    query = None
    if item_category == "weapon":
        query = ("UPDATE MountedItems "
                 "SET weapon_slot = (%s) "
                 "WHERE user_id = (%s);")
    elif item_category == "armor":
        query = ("UPDATE MountedItems "
                 "SET armor_slot = (%s) "
                 "WHERE user_id = (%s);")
    elif item_category == "color":
        query = ("UPDATE MountedItems "
                 "SET color_slot = (%s) "
                 "WHERE user_id = (%s);")
    else:
        return False

    mount_data = (item.item_id, user_id)

    connection = database.Connection()
    connection.cursor.execute(query, mount_data)
    connection.connection.commit()
    connection.close()
    return True

def get_mounted_items_from_database(user_id):
    mounted_items = {"armor":0, "weapon":0, "color":0}
    query = "SELECT * FROM MountedItems WHERE user_id=(%s);"

    connection = database.Connection()
    connection.cursor.execute(query, (user_id,))
    item_rows = connection.cursor.fetchall()
    connection.close()

    if len(item_rows) == 0:
        return mounted_items

    mounted_items["weapon"] = item_rows[0][1]
    mounted_items["armor"] = item_rows[0][2]
    mounted_items["color"] = item_rows[0][3]
    return mounted_items

def get_items_from_data_base(user_id):
    items = {}
    query = "SELECT * FROM UserItems WHERE user_id=(%s);"

    connection = database.Connection()
    connection.cursor.execute(query, (user_id,))
    item_rows = connection.cursor.fetchall()

    for item_data in item_rows:
        garage_items = garage_item_loader.get_item_by_id(item_data[1])
        item = database_garage_item.DatabaseGarageItem(garage_items)
        item.item_id = item_data[1]
        item.upgrading_property_id = item_data[2]
        item.upgrade_done_time = item_data[3]
        item.property_levels_id = item_data[4]
        item.count = item_data[5]
        item.temporary_item_expiration_time = item_data[6]
        item.upgradable_property_data_levels = {}

        if not item.property_levels_id == None:
            query = "SELECT * FROM PropertyLevels WHERE id=(%s);"
            connection.cursor.execute(query, (item.property_levels_id,))
            property_levels = connection.cursor.fetchall()

            for property in property_levels:
                property_id = property[1]
                property_level = property[2]

                item.upgradable_property_data_levels[property_id] = property_level

        items[item.item_id] = item

    connection.close()
    return items

def remove_item(item, user_id):
    query = "DELETE FROM UserItems WHERE item_id=(%s) AND user_id=(%s);"

    connection = database.Connection()
    connection.cursor.execute( query, (item.item_id, user_id) )

    if item.property_levels_id:
        query = "DELETE FROM PropertyLevels WHERE id=(%s);"
        connection.cursor.execute( query, (item.property_levels_id,) )

    connection.connection.commit()
    connection.close()
