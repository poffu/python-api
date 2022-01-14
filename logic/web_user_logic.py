from dao import web_user_dao
from model import web_user_dto


class WebUserLogic:

    def __init__(self):
        self.__web_user_dao = web_user_dao.WebUserDao()

    def login(self, user: web_user_dto.LoginDto):
        return self.__web_user_dao.login(user)

    def insert(self, user: web_user_dto.InsertDto):
        return self.__web_user_dao.insert(user)

    def check_email(self, userId, email):
        return self.__web_user_dao.check_email(userId, email)

    def get_all_user(self, name):
        return self.__web_user_dao.get_all_user(name)

    def get_user(self, userId):
        return self.__web_user_dao.get_user(userId)

    def update(self, user: web_user_dto.UpdateDto):
        return self.__web_user_dao.update(user)

    def delete(self, userId):
        return self.__web_user_dao.delete(userId)
