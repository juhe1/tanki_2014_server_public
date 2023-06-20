from database import database

def create_new_user_property(user_properties):
    user_properties = (user_properties["id"], user_properties["crystals"], user_properties["score"],
                       user_properties["last_visit"], user_properties["next_crystal_reward"], user_properties["user_roles"])

    query = ("INSERT INTO UserProperties (id, crystals, score, last_visit, next_crystal_reward, user_roles)"
             "VALUES (%s, %s, %s, %s, %s, %s)")

    connection = database.Connection()
    connection.cursor.execute(query, user_properties)
    connection.connection.commit()
    connection.close()

def get_atribute_by_id(_id, attribute):
    connection = database.Connection()
    connection.cursor.execute("SELECT " + attribute + " FROM UserProperties WHERE id = (%s)", (_id,))
    rows = connection.cursor.fetchall()
    connection.close()

    if not len(rows) == 0:
        return rows[0][0]

def set_crystal_count(crystal_count, user_id):
    query = ("UPDATE UserProperties "
             "SET crystals = (%s) "
             "WHERE id = (%s);")
    data = (crystal_count, user_id)

    connection = database.Connection()
    connection.cursor.execute(query, data)
    connection.connection.commit()
    connection.close()

def add_crystals(crystals, user_id):
    if crystals < 0: return

    query = ("UPDATE UserProperties "
             "SET crystals = crystals + (%s) "
             "WHERE id = (%s);")
    data = (crystals, user_id)

    connection = database.Connection()
    connection.cursor.execute(query, data)
    connection.connection.commit()
    connection.close()

def set_score(score, user_id):
    query = ("UPDATE UserProperties "
             "SET score = (%s) "
             "WHERE id = (%s);")
    data = (score, user_id)

    connection = database.Connection()
    connection.cursor.execute(query, data)
    connection.connection.commit()
    connection.close()
