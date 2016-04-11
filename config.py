import os


basedir = os.path.abspath(os.path.dirname(__file__))


def read(fname):
    with open(os.path.join(basedir, fname)) as stream:
        return stream.read()


class Config:

    SECRET_KEY = os.environ.get("SECRET_KEY") or read("etc/secret.key")
    DATABASE_URI = "sqlite://:memory:"
    SSL_DISABLE = False
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

    @staticmethod
    def init_app(app):
        pass


class ProductionConfig(Config):

    DATABASE_URI = 'sqlite://' + os.path.join(basedir, "coliw.db")


class DevelopmentConfig(Config):

    DEBUG = True


class TestingConfig(Config):

    TESTING = True
    WTF_CSRF_ENABLED = False


config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
