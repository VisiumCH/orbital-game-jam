import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:

    def __init__(self):
        self.DEBUG = False
        self.TESTING = False
        self.CSRF_ENABLED = True
        self.SECRET_KEY = 'this-really-needs-to-be-changed'


class ProductionConfig(Config):
    Config.DEBUG = False


class StagingConfig(Config):
    Config.DEVELOPMENT = True
    Config.DEBUG = True


class DevelopmentConfig(Config):
    Config.DEVELOPMENT = True
    Config.DEBUG = True


class TestingConfig(Config):
    Config.TESTING = True
