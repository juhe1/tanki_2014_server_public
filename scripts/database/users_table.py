from database import database

def create_new_user(user):
    user_tuple = (user["name"], user["password"], user["email"], user["reg_date"])

    connection = database.Connection()
    connection.cursor.execute("INSERT INTO Users (username, password, email, reg_date) VALUES (%s, %s, %s, %s)", user_tuple)
    connection.connection.commit()
    connection.close()

def user_exist(username):
    connection = database.Connection()
    connection.cursor.execute("SELECT EXISTS(SELECT * FROM Users WHERE username = (%s))", (username,))
    rows = connection.cursor.fetchall()
    connection.close()

    return not rows[0] == (0,)

def get_atribute_by_username(username, attribute):
    connection = database.Connection()
    connection.cursor.execute("SELECT " + attribute + " FROM Users WHERE username = (%s)", (username,))
    rows = connection.cursor.fetchall()
    connection.close()

    if not len(rows) == 0:
        return rows[0][0]
