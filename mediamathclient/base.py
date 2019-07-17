import terminalone

class Base:
    def __init__(self, api_key, username, password, data=None):
        self.api_key = api_key
        self.username = username
        self.password = password
        self.data = data

    def get_connection(self):
        creds = {
            "username": self.username,
            "password": self.password,
            "api_key": self.api_key
        }
        return terminalone.T1(auth_method="cookie", **creds)
