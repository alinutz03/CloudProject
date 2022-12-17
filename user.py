import pam

class User:
    def init(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def login(self):
        res_auth = pam.authenticate(username=self.username, password=self.password)
        return res_auth

class Login:

    def __init__(self,method=None):
        self.authmethod=method

    def login(self):
        res_login=self.authmethod.login()

        return res_login

    def __init__(self,method):
        self.authmethod=method()