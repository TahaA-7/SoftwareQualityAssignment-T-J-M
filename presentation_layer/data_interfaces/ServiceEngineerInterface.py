import logic_layer.utils.StringValidations as StringValidations

class ServiceEngineerInterface():
    # service engineer is standard user
    def __init__(self, ):
        pass

    def start(self):
        pass

    def update_self_password(self):
        new_password = input("Please enter new password")
        if StringValidations.is_valid_password(new_password):
            return False
        else:
            # update_password
            pass

    def update_scooter_attributes(self):
        # if user is service engineer, rights are limited
        pass

    def view_scooter(self):
        # search scooter info
        '''
        Note 2: The search function must accept reasonable data fields as a search key. It must also accept
        partial keys. For example, a user can search for a Traveller with a name “Mike Thomson” and customer
        ID “2123287421” by entering any of these keys: “mik”, “omso”, or “2328”, etc.
        '''
        pass

    def foo(self):
        print("hi")
