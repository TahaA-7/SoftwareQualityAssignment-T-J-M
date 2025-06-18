class Session:
    logged_in = False
    user = None

    @classmethod
    def set_loggedin_true(cls, fetched_user=None):
        cls.logged_in = True
        cls.user = fetched_user

    @classmethod
    def set_loggedin_false(cls):
        cls.logged_in = False
        cls.user = None
