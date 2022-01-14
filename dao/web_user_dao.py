import collections
from dao import connection_dao
from model import web_user_dto


def EscapeSqlLike(text):
    return text.replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_')


class WebUserDao:

    def __init__(self):
        self.__connection_dao = connection_dao.ConnectionDao()

    def login(self, user: web_user_dto.LoginDto):
        data = None
        self.__connection_dao.connection_postgre()
        if self.__connection_dao.conn is not None:
            try:
                self.__connection_dao.conn.autocommit = True
                cursor = self.__connection_dao.conn.cursor()
                sql = "SELECT user_id, name, email, tel FROM web_user " \
                      "WHERE rule = 0 AND email = %s AND password = %s LIMIT 1"
                cursor.execute(sql, (user.email, user.password))
                result = cursor.fetchone()
                if result is not None:
                    data = {"userId": result[0], "name": result[1], "email": result[2], "tel": result[3]}
                cursor.close()
            finally:
                self.__connection_dao.close_connection()
        return data

    def insert(self, user: web_user_dto.InsertDto):
        check = False
        self.__connection_dao.connection_postgre()
        if self.__connection_dao.conn is not None:
            try:
                self.__connection_dao.conn.autocommit = True
                cursor = self.__connection_dao.conn.cursor()
                sql = "INSERT INTO web_user (email, name, password, tel, rule) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (user.email, user.name, user.password, user.tel, 1))
                check = True
                cursor.close()
            finally:
                self.__connection_dao.close_connection()
        return check

    def check_email(self, userId, email):
        check = False
        self.__connection_dao.connection_postgre()
        if self.__connection_dao.conn is not None:
            try:
                self.__connection_dao.conn.autocommit = True
                cursor = self.__connection_dao.conn.cursor()
                sql = "SELECT user_id FROM web_user WHERE email = %s AND user_id != %s LIMIT 1"
                cursor.execute(sql, (email, userId))
                if cursor.fetchone() is not None:
                    check = True
                cursor.close()
            finally:
                self.__connection_dao.close_connection()
        return check

    def get_all_user(self, name):
        users_list = []
        self.__connection_dao.connection_postgre()
        if self.__connection_dao.conn is not None:
            try:
                self.__connection_dao.conn.autocommit = True
                cursor = self.__connection_dao.conn.cursor()
                sql = "SELECT user_id, name, email, tel  FROM web_user " \
                      "WHERE rule = 1 AND name ILIKE %(name)s ORDER BY LOWER(name) ASC, LOWER(email) ASC"
                cursor.execute(sql, {'name': '%{}%'.format(EscapeSqlLike(name))})
                results = cursor.fetchall()
                for row in results:
                    d = collections.OrderedDict()
                    d["userId"] = row[0]
                    d["name"] = row[1]
                    d["email"] = row[2]
                    d["tel"] = row[3]
                    users_list.append(d)
                cursor.close()
                return users_list
            finally:
                self.__connection_dao.close_connection()

    def get_user(self, userId):
        user = {}
        self.__connection_dao.connection_postgre()
        if self.__connection_dao.conn is not None:
            try:
                self.__connection_dao.conn.autocommit = True
                cursor = self.__connection_dao.conn.cursor()
                sql = "SELECT user_id, name, email, tel FROM web_user WHERE rule = 1 AND user_id = %s LIMIT 1"
                cursor.execute(sql, [userId])
                result = cursor.fetchone()
                if result is not None:
                    user["userId"] = result[0]
                    user["name"] = result[1]
                    user["email"] = result[2]
                    user["tel"] = result[3]
                cursor.close()
            finally:
                self.__connection_dao.close_connection()
        return user

    def update(self, user: web_user_dto.UpdateDto):
        check = False
        self.__connection_dao.connection_postgre()
        if self.__connection_dao.conn is not None:
            try:
                self.__connection_dao.conn.autocommit = True
                cursor = self.__connection_dao.conn.cursor()
                if len(user.password) == 0:
                    sql = "UPDATE web_user SET (email, name, tel) = (%s, %s, %s) WHERE user_id = %s"
                    cursor.execute(sql, [user.email, user.name, user.tel, user.userId])
                else:
                    sql = "UPDATE web_user SET (email, name, password, tel) = (%s, %s, %s, %s) WHERE user_id = %s"
                    cursor.execute(sql, [user.email, user.name, user.password, user.tel, user.userId])
                check = True
                cursor.close()
            finally:
                self.__connection_dao.close_connection()
        return check

    def delete(self, userId):
        check = False
        self.__connection_dao.connection_postgre()
        if self.__connection_dao.conn is not None:
            try:
                self.__connection_dao.conn.autocommit = True
                cursor = self.__connection_dao.conn.cursor()
                sql = "DELETE FROM web_user  WHERE rule = 1 AND user_id = %s"
                cursor.execute(sql, [userId])
                check = True
                cursor.close()
            finally:
                self.__connection_dao.close_connection()
        return check
