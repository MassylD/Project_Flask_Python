from flask_app.models import user
from flask_app.config.mysqlconnection import connectToMySQL


class Painting:
    db = "painting_db"
    table_name = "PAINTING"

    def __init__(self, data) -> None:
        self.id = data["ID"]
        self.title = data["TITLE"]
        self.description = data["DESCRIPTION"]
        self.price = data["PRICE"]
        self.user = user.User.get_by_id({'id': data["USER_ID"]})

    # CRUD ----
    @classmethod
    def create(cls, data):
        query = f"INSERT INTO {cls.table_name} (TITLE, DESCRIPTION, PRICE, USER_ID) VALUES (%(title)s, %(description)s, %(price)s, %(user_id)s)"
        result = connectToMySQL(cls.db).query_db(query, data)
        return result

    @classmethod
    def edit(cls, data):
        query = f"UPDATE {cls.table_name} SET TITLE=%(title)s, DESCRIPTION=%(description)s, PRICE=%(price)s WHERE ID=%(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results[0] if results else None

    @classmethod
    def delete(cls, data):
        query = f"DELETE FROM {cls.table_name} WHERE ID=%(id)s"
        connectToMySQL(cls.db).query_db(query, data)
        return

    @classmethod
    def get_all(cls):
        query = f"SELECT * FROM {cls.table_name}"
        data = connectToMySQL(cls.db).query_db(query)
        data_list = []
        if data:
            for d in data:
                data_list.append(cls(d))

        return data_list

    @classmethod
    def get_by_user(cls, data):
        query = f"SELECT * FROM {cls.table_name} WHERE USER_ID=%(user_id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        data_list = []
        if data:
            for d in results:
                data_list.append(cls(d))

        return data_list if data_list else None

    @classmethod
    def get_by_id(cls, data):
        query = f"SELECT * FROM {cls.table_name} WHERE ID=%(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0]) if results else None
