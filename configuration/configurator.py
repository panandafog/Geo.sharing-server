import os

def is_testing():
    return os.environ["CONFIG_TYPE"] == 'testing'

def set_testing(testing):
    if testing:
        os.environ["CONFIG_TYPE"] = 'testing'
    else:
        os.environ["CONFIG_TYPE"] = 'production'

class Configurator:

    def __init__(self):
        self.db_host = 'localhost'
        self.db_username = 'geo'
        self.db_password = 'password'
        self.db_name = 'geo_db'

        if is_testing():
            self.db_port = '27018'
        else:
            self.db_port = '27017'

        self.db_uri = "mongodb://" + \
                      str(self.db_username) + ":" + str(self.db_password) + \
                      "@" + str(self.db_host) + ":" + str(self.db_port) + \
                      "/" + str(self.db_name)
