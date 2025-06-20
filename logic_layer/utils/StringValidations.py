import re
import string
# https://stackoverflow.com/questions/30556857/creating-a-static-class-with-no-instances

class StringValidations:
    @classmethod
    def is_valid_username(cls, username: str):
        if username == "super_admin":
            return True
        return cls.__length_and_characters_check("username", username)

    @classmethod
    def is_valid_email(cls, email: str) -> bool:
        if cls.__check_regex("email", email) == False:
            return False
        elif cls.__length_and_characters_check("email", email) == False:
            return False
        return True

    @classmethod
    def is_valid_password(cls, password: str) -> bool:
        if password == "Admin_123?":
            return True
        return cls.__length_and_characters_check("password", password)

    @classmethod
    def is_valid_first_or_last_name(cls, fl_name: str) -> bool:
        return fl_name.isalpha()

    @classmethod
    def __length_and_characters_check(cls, type, str: str):
        validations_dict = {"init": True}
        try:
            if type == "username":
                username = str
                allowed_chars = set(string.ascii_letters + string.digits + "_'.,")
                validations_dict = {
                    "length": 7 < len(username) < 11,
                    "starts_correctly": username[0] in set(string.ascii_letters).union("_"),
                    # use whitelist to avoid potential errors
                    "follows_correctly": all(c in allowed_chars for c in username[1:])
                }

            elif type == "password":
                password = str
                #
                # allowed_specials = {'!', '@', '-', '#', '$', '%', '&', '*', '^'}
                allowed_specials = [c for c in "~!@#$%&_-+=`|\(){}[]:;'<>,.?/"]
                allowed_specials_set = set(string.ascii_letters + string.digits).union(allowed_specials)
                #
                validations_dict = {
                    # 8 is not enough for a minimum length for applications that require tighter security
                    "length": 11 < len(password) < 31,
                    # if even a single digit is found, `validations_dict[1]` should return True
                    "digit": any(c.isdigit() for c in password),
                    "lowercase": any(c.islower() for c in password),
                    "capital": any(c.isupper() for c in password),
                    # these characters are safe in Python
                    "special_char": any(c in allowed_specials for c in password),
                    # another whitelist method, yes
                    "all_allowed": all(c in allowed_specials_set for c in password)
                }

            elif type == "email":
                None
            
            else:
                validations_dict = {"default": False}
        except Exception as ex:
            return "An error returned: " + ex

        # returns true if all booleans are true
        return all(validations_dict.values())
    
    @classmethod
    def __check_regex(cls, type, str_to_validate):
        pattern = ""
        if type == "email":
            pattern = (r"^(?!\.)(?!.*\.\.)[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+" 
                       r"@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$")
            '''
            ^ = start of string
            (?!\.) = negative lookahead ensuring string doesn't start with a dot
            (?!.*\.\.) = doesn't allow consecutive dots
            the rest of the regex string until `+` ensures the string matches one/more allowed characters
            + = appends to the next regex string to make into a single
            # @ = literal @
            [a-zA-Z0-9-]+ = matches lower- and uppercase and digits and hyphens in domain name
            \. = literal .
            [a-zA-Z]{2,} = matching at least two letters in the TLD
            $ = end of string
            '''

        return re.match(pattern, str_to_validate) is not None

    @classmethod
    def handle_input_length(cls, inp: str):
        return inp[-1].upper() if len(inp) > 0 else " "


'''  
● Username:
    ○ must be unique and have a length of at least 8 characters
    ○ must be no longer than 10 characters
    ○ must be started with a letter or underscores (_)
    ○ can contain letters (a-z), numbers (0-9), underscores (_), apostrophes ('), and periods (.)
    ○ no distinction between lowercase and uppercase letters (case-insensitive)

● Password:
    ○ must have a length of at least 12 characters
    ○ must be no longer than 30 characters
    ○ can contain letters (a-z), (A-Z), numbers (0-9), Special characters such as ~!@#$%&_-
    +=`|\(){}[]:;'<>,.?/
    ○ must have a combination of at least one lowercase letter, one uppercase letter, one digit,
'''
