from DataModels.UserModel import User
from utils.Roles import Roles

class Session:
    logged_in = False
    user = None

    @classmethod
    def set_loggedin_true(cls, fetched_user=None):
        cls.logged_in = True
        cls.user = fetched_user if isinstance(fetched_user, User) else User(
            fetched_user['username'], fetched_user['password'], "", "", fetched_user['role'], True)
        cls.user.role = Roles(cls.user.role)

    @classmethod
    def set_loggedin_false(cls):
        cls.logged_in = False
        cls.user = None
