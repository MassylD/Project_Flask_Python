from flask_app.config.mysqlconnection import connectToMySQL


class User:
    db = "painting_db"
    table_name = "USER"

    def __init__(self, data) -> None:
        self.id = data["ID"]
        self.email = data["EMAIL"]
        self.password = data["PASSWORD"]
        self.first_name = data["FIRST_NAME"]
        self.last_name = data["LAST_NAME"]
        self.created_at = data["CREATED_AT"]
        self.updated_at = data["UPDATED_AT"]

    # CRUD ----
    @classmethod
    def create(cls, data):
        print(data)
        query = f"INSERT INTO {cls.table_name} (FIRST_NAME, LAST_NAME, EMAIL, PASSWORD) VALUES (%(first_name)s,%(last_name)s, %(email)s, %(password)s);"
        result = connectToMySQL(cls.db).query_db(query, data)
        return result

    @classmethod
    def get_by_email(cls, data):
        query = f"SELECT * FROM {cls.table_name} WHERE EMAIL=%(email)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0]) if results else False

    @classmethod
    def get_by_id(cls, data):
        query = f"SELECT * FROM {cls.table_name} WHERE ID=%(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0]) if results else False
