from .entities.users import User

class ModelUsers:
    @classmethod
    def login(cls, db, user):
        try:
            cursor = db.connection.cursor()
            cursor.execute("CALL sp_verifyIdentity(%s, %s)", (user.username, user.password))
            row = cursor.fetchone()
            if row is not None and len(row) >= 5:
                user = User(row[0], row[1], row[2], row[4], row[3])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception("Error during login: " + str(ex))

    @classmethod
    def get_by_id(cls, db, id):
        try:
            cursor = db.connection.cursor()
            cursor.execute("SELECT id, username, usertype, fullname FROM users WHERE id = %s", (id,))
            row = cursor.fetchone()
            if row is not None:
                return User(row[0], row[1], None, row[2], row[3])
            else:
                return None
        except Exception as ex:
            raise Exception("Error fetching user by ID: " + str(ex))


    @classmethod
    def get_all_users(self, db):
        try:
            cursor = db.connection.cursor()
            cursor.execute("SELECT id, username, usertype, fullname FROM users")
            rows = cursor.fetchall()
            users = []
            for row in rows:
                users.append(User(row[0], row[1], None, row[2], row[3]))
            return users
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def add_user(self, db, user):
        try:
            cursor = db.connection.cursor()
            cursor.execute("CALL sp_AddUser(%s, %s, %s, %s)", (user.username, user.password, user.fullname, user.usertype))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def update_user(self, db, user):
        try:
            cursor = db.connection.cursor()
            cursor.execute("UPDATE users SET username = %s, fullname = %s, usertype = %s WHERE id = %s", 
                           (user.username, user.fullname, user.usertype, user.id))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def delete_user(self, db, id):
        try:
            cursor = db.connection.cursor()
            cursor.execute("DELETE FROM users WHERE id = %s", (id,))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)
