db_name = 'rpn-calculator.db'
db_test_name = ':memory:'


class Config(object):
    FLASK_ENV = 'development'
    DEBUG = False
    TESTING = False

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_name}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    FLASK_ENV = 'production'


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_test_name}"
    WTF_CSRF_ENABLED = False
