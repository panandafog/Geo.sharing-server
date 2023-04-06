import os


class Configurator:

    def __init__(self):
        self.db_host = 'localhost'
        self.db_port = '27017'
        self.db_username = 'geo'
        self.db_password = 'password'
        self.db_name = 'geo_db'
        self.db_uri = "mongodb://" + \
                      str(self.db_username) + ":" + str(self.db_password) + \
                      "@" + str(self.db_host) + ":" + str(self.db_port) + \
                      "/" + str(self.db_name)
