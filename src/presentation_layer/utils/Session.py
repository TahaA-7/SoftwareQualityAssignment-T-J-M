from DataModels.UserModel import User
from presentation_layer.utils.Roles import Roles

class Session:
    logged_in = False
    user = None

    @classmethod
    def set_loggedin_true(cls, fetched_user=None):
        cls.logged_in = True
        cls.user = fetched_user if isinstance(fetched_user, User) else User(
            fetched_user['username'], fetched_user['password'], "", "", fetched_user['role'], True)
        if not isinstance(cls.user.role, Roles):
            try:
                # Try integer conversion first
                cls.user.role = Roles(int(cls.user.role))
            except (ValueError, TypeError):
                # Try by name (string) if int conversion fails
                cls.user.role = Roles[cls.user.role]

    @classmethod
    def set_loggedin_false(cls):
        cls.logged_in = False
        cls.user = None
